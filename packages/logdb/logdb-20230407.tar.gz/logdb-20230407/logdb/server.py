import os
import sys
import ssl
import time
import uuid
import json
import sanic
import signal
import pickle
import random
import hashlib
import sqlite3
import asyncio
import aiohttp
import logging
from sanic.exceptions import Unauthorized


APP = sanic.Sanic('logdb')


# Global variables
class G:
    seq = None
    ssl_ctx = None
    session = None
    servers = set()
    default_seq = '00000000-000000'
    learned_seq = '99999999-999999'
    db = sqlite3.connect('db.sqlite3')


# Update file the most reliable way possible.
def paxos_file_update(path, promised_seq, accepted_seq, accepted_val=None):
    hdr = '{}\n{}\n'.format(promised_seq, accepted_seq).encode()
    assert(32 == len(hdr))

    # File does not exist or needs to be fully rewritten,
    # Create a tmp file and then rename it
    if not os.path.isfile(path) or accepted_val is not None:
        tmpfile = '{}-{}.tmp'.format(path, uuid.uuid4())
        with open(tmpfile, 'wb') as fd:
            fd.write(hdr)

            if accepted_val:
                fd.write(accepted_val)
        os.rename(tmpfile, path)

    # File already exists
    else:
        with open(path, 'r+b') as fd:
            fd.write(hdr)


# PAXOS Acceptor and Learner
@APP.post('/paxos/<phase:str>/<proposal_seq:str>/<path:path>')
async def paxos_server(request, phase, proposal_seq, path):
    if request:
        peer = get_peer(request)

    if request and peer is not None and peer not in G.servers:
        raise Unauthorized('')

    def decode(buf):
        return buf.decode().strip('\n')

    os.makedirs(os.path.dirname(path), exist_ok=True)

    promised_seq = accepted_seq = G.default_seq
    if os.path.isfile(path):
        with open(path, 'rb') as fd:
            promised_seq = decode(fd.read(16))
            accepted_seq = decode(fd.read(16))

            # Hack. Just reusing the code. Not related to paxos.
            if G.learned_seq == promised_seq == accepted_seq:
                if 'fetch' == phase:
                    return response(fd.read()) if request else fd.read()

                return response('ALREADY_LEARNED')

    # Paxos standard - phase 1
    if 'promise' == phase and proposal_seq > promised_seq:
        paxos_file_update(path, proposal_seq, accepted_seq)

        with open(path, 'rb') as fd:
            promised_seq = decode(fd.read(16))
            accepted_seq = decode(fd.read(16))

            return response([accepted_seq, fd.read()])

    # Paxos standard - phase 2
    if 'accept' == phase and proposal_seq == promised_seq:
        paxos_file_update(path, proposal_seq, proposal_seq,
                          pickle.loads(request.body))

        return response('OK')

    # Paxos protocol is already complete. This is a custom learn step.
    if 'learn' == phase and proposal_seq == promised_seq == accepted_seq:
        # This paxos round completed. Mark this value as final.
        # Set promise_seq = accepted_seq = '99999999-999999'
        # This is the largest possible value for seq and would ensure
        # tha any subsequent paxos rounds get rejected.
        paxos_file_update(path, G.learned_seq, G.learned_seq)

        return response('OK')


# PAXOS Proposer
async def paxos_client(path, value):
    quorum = int(len(G.servers)/2) + 1

    url = 'paxos/{{}}/{}/{}'.format(time.strftime('%Y%m%d-%H%M%S'), path)

    res = await rpc(url.format('promise'))
    if quorum > len(res):
        return 'NO_PROMISE_QUORUM'

    if 'ALREADY_LEARNED' in res.values():
        return 'ALREADY_LEARNED'

    proposal = (G.default_seq, value)
    for accepted_seq, accepted_val in res.values():
        if accepted_seq > proposal[0]:
            proposal = (accepted_seq, accepted_val)

    if quorum > len(await rpc(url.format('accept'), proposal[1])):
        return 'NO_ACCEPT_QUORUM'

    # No need to check the result of this.
    # PAXOS round has already completed.  If a node doesn't learn
    # the value, another paxos round would be run at the read time.
    await rpc(url.format('learn'))

    return 'CONFLICT' if value is not proposal[1] else 'OK'


# Write the file reliably at a majority of the nodes.
async def cluster_write(path, tags, value):
    tags['length'] = len(value)
    tags['datetime'] = int(time.strftime('%Y%m%d%H%M%S'))

    return await paxos_client(path, json.dumps(tags).encode() + b'\n' + value)


# Read the file if it was written successfully earlier.
# If it does not exist, create the file with empty content.
async def cluster_read(path):
    for i in range(2):
        # Return if this file is already learned and this node has it
        buf = await paxos_server(None, 'fetch', 0, path)
        if buf:
            hdr, vbuf = buf.split(b'\n', maxsplit=1)
            return json.loads(hdr.decode()), vbuf, 32+len(buf)

        # If the value is already learned by a majority of nodes,
        # but this node does it have it, fetch it from other nodes.
        for j in range(len(G.servers)):
            srv = random.choice(list(G.servers))
            res = await rpc('paxos/fetch/0/{}'.format(path), servers=[srv])
            if res:
                paxos_file_update(path, G.learned_seq, G.learned_seq, res[srv])
                break

        # No node has learned the value. No paxos round completed for this.
        # Lets run a paxos round with empty value. If a previous paxos round
        # failed mid-way, value proposed in that round would be learned.
        # Otherwise, this log entry would be marked empty.
        if j == len(G.servers) - 1:
            await cluster_write(path, dict(), b'')


# Background task to index the tags for quick search
# If this node does not have the file yet, fetches it from
# other nodes in the cluster, if it was successfully writter earlier.
# If it was not written yet, creates it with empty content.
async def sync_and_index():
    G.db.execute('''create table if not exists channels(
                    seq  integer primary key,
                    date integer not null,
                    hash integer not null)''')
    G.db.execute('create index if not exists c0 on channels(hash)')

    G.db.execute('''create table if not exists tags(
                    hash blob primary key,
                    seq  integer)''')

    commit_timestamp = time.time()
    while True:
        seq = G.db.execute('select max(seq) from channels').fetchone()
        seq = -1 if seq[0] is None else seq[0]
        seq += 1

        # We have some log entries to index
        while seq <= G.seq:
            path = os.path.join('log', str(int(seq/10000)), str(seq))
            tags, blob, length = await cluster_read(path)

            date = int(tags['datetime'] / 1000000)
            channel = tags.get('reader', '') + tags.get('channel', '')
            channel_hash = hashlib.sha256(channel.encode()).digest()
            channel_hash = int.from_bytes(channel_hash[28:], 'big')
            channel_hash = channel_hash % (2*1000*1000*1000)

            G.db.execute('''insert or ignore into channels(seq,date,hash)
                            values(?,?,?)''', (seq, date, channel_hash))

            writer = tags.get('writer', '') + channel
            writer_hash = hashlib.sha256(writer.encode()).digest()

            G.db.execute('insert or replace into tags(hash, seq) values(?,?)',
                         (writer_hash, seq))

            logging.critical((seq, tags))
            seq += 1

            if time.time() > commit_timestamp + 1:
                G.db.commit()
                commit_timestamp = time.time()
                logging.critical('synced seq({})'.format(seq))

        G.db.commit()
        seq -= 1

        # Indexed available log entries, wait for more to arrive.
        res = await rpc('seq/max')
        G.seq = max(G.seq, max(res.values()))

        for i in range(15):
            if G.seq > seq:
                break

            await asyncio.sleep(1)


def response(obj):
    return sanic.response.raw(pickle.dumps(obj))


def get_peer(request):
    if 'http' == request.scheme:
        return None

    cert = request.transport.get_extra_info('peercert')
    return dict(cert['subject'][0])['commonName']


async def rpc(url, obj=None, servers=None):
    servers = servers if servers else G.servers

    if G.session is None:
        if os.path.isfile('ca.pem'):
            G.ssl_ctx = ssl.create_default_context(
                cafile='ca.pem',
                purpose=ssl.Purpose.SERVER_AUTH)
            G.ssl_ctx.load_cert_chain('client.pem', 'client.key')
            G.ssl_ctx.verify_mode = ssl.CERT_REQUIRED

        G.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=1000))

    scheme = 'https' if G.ssl_ctx else 'http'
    responses = await asyncio.gather(
        *[asyncio.ensure_future(
          G.session.post('{}://{}/{}'.format(scheme, s, url),
                         data=pickle.dumps(obj), ssl=G.ssl_ctx))
          for s in servers],
        return_exceptions=True)

    result = dict()
    for s, r in zip(servers, responses):
        if type(r) is aiohttp.client_reqrep.ClientResponse:
            if 200 == r.status:
                result[s] = pickle.loads(await r.read())

    return result


@APP.post('/seq/<which:str>')
async def seq(request, which):
    peer = get_peer(request)

    if peer is not None and peer not in G.servers:
        raise Unauthorized('')

    if 'next' == which:
        G.seq += 1

    return response(G.seq)


@APP.post('/')
async def append(request):
    peer = get_peer(request)

    tags = dict()
    for k in request.args:
        tags[k] = request.args.get(k)

    if peer:
        tags['writer'] = peer

    if 'reader' not in tags and 'writer' in tags:
        tags['reader'] = tags['writer']

    res = await rpc('seq/next')
    seq = max(res.values())
    path = os.path.join('log', str(int(seq / 10000)), str(seq))

    if 'OK' == await cluster_write(path, tags, request.body):
        return sanic.response.json(seq, headers={'x-seq': seq})


@APP.put('/<path:path>/<version:int>')
async def put(request, path, version):
    peer = get_peer(request)
    peer = peer if peer else ''
    path = os.path.join('kv', peer, path.strip('/'), str(int(version)))

    status = await cluster_write(path, dict(), request.body)
    return sanic.response.empty(headers={'x-status': status})


@APP.post('/version/<path:path>')
async def version(request, path):
    peer = get_peer(request)

    if peer is not None and peer not in G.servers:
        raise Unauthorized('')

    path = path.strip('/')
    files = [int(f) for f in os.listdir(path) if f.isdigit()]

    for version in sorted(files, reverse=True):
        if os.stat(os.path.join(path, str(version))).st_size > 32:
            for f in files:
                if f < version:
                    os.remove(os.path.join(path, str(f)))

            return response(version)


@APP.get('/<path:path>')
async def get(request, path):
    peer = get_peer(request)
    peer = peer if peer else ''
    path = os.path.join('kv', peer, path.strip('/'))

    res = await rpc('version//{}'.format(path))
    ver = max(res.values())

    tags, blob, _ = await cluster_read(os.path.join(path, str(ver)))
    tags = {'x-'+k: v for k, v in tags.items()}
    tags['x-seq'] = ver

    return sanic.response.raw(blob, headers=tags)


@APP.get('/')
async def tags(request):
    peer = get_peer(request)

    res = await rpc('seq/max')
    seq = -1

    while seq < max(res.values()):
        await asyncio.sleep(1)

        seq = G.db.execute('select max(seq) from tags').fetchone()
        seq = -1 if seq[0] is None else seq[0]

    writer = peer if peer else ''
    writer += request.args.get('reader', writer)
    writer += request.args.get('channel', '')
    writer_hash = hashlib.sha256(writer.encode()).digest()

    seq = G.db.execute('select seq from tags where hash=?',
                       [writer_hash]).fetchone()[0]

    if seq:
        path = os.path.join('log', str(int(seq/10000)), str(seq))
        tags_obj, blob, _ = await cluster_read(path)
        tags_json = json.dumps(tags_obj, sort_keys=True, indent=4)

        return sanic.response.raw(tags_json, headers={'x-seq': seq})


@APP.get('/<seq:int>')
async def tail(request, seq):
    seq = int(seq)
    peer = get_peer(request)

    reader = peer if peer else ''
    channel = request.args.get('channel', '')
    channel_hash = hashlib.sha256((reader + channel).encode()).digest()
    channel_hash = int.from_bytes(channel_hash[28:], 'big')
    channel_hash = channel_hash % (2*1000*1000*1000)

    while True:
        seq = G.db.execute('''select seq from channels where hash=? and
                              seq >= ? order by seq limit 1
                           ''', (channel_hash, seq)).fetchone()

        if seq is None or seq[0] is None:
            return

        seq = seq[0]
        path = os.path.join('log', str(int(seq/10000)), str(seq))
        tags, blob, _ = await cluster_read(path)

        if reader == tags.get('reader', ''):
            if channel == tags.get('channel', ''):
                tags = {'x-'+k: v for k, v in tags.items()}
                tags['x-seq'] = seq
                return sanic.response.raw(blob, headers=tags)

        seq += 1
        logging.critical('Rare HASH Conflict at seq(%d)', seq)


if '__main__' == __name__:
    G.servers = set()
    for i in range(2, len(sys.argv)):
        G.servers.add(sys.argv[i])

    G.host, G.port = sys.argv[1].split(':')
    G.port = int(G.port)

    G.seq = 0
    os.makedirs('kv', exist_ok=True)
    os.makedirs('log', exist_ok=True)

    # Find out the latest file
    for d in sorted([int(x) for x in os.listdir('log')], reverse=True):
        path = os.path.join('log', str(d))
        files = [int(x) for x in os.listdir(path) if x.isdigit()]
        if files:
            G.seq = max(files)
            break

    ssl_ctx = None
    if os.path.isfile('ca.pem'):
        ssl_ctx = ssl.create_default_context(
            cafile='ca.pem',
            purpose=ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain('server.pem', 'server.key')
        ssl_ctx.verify_mode = ssl.CERT_REQUIRED

    signal.alarm(random.randint(1, 3600))
    APP.add_task(sync_and_index())

    for i, srv in enumerate(sorted(G.servers)):
        logging.critical('cluster node({}) : {}'.format(i+1, srv))
    logging.critical('server({}:{}) seq({})'.format(G.host, G.port, G.seq))
    APP.run(host=G.host, port=G.port, single_process=True, access_log=True,
            ssl=ssl_ctx)
