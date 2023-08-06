import os
import random
import requests

requests.packages.urllib3.disable_warnings()


def extract_response(req):
    res = dict(blob=req.content)

    for k, v in req.headers.items():
        if k.startswith('x-'):
            res[k[2:]] = v

    return res


class Client:
    def __init__(self, servers, ca_pem=None, client_pem=None, client_key=None):
        self.servers = servers
        self.session = requests.Session()
        self.url_type = 'http'

        ca_pem = ca_pem if ca_pem else 'ca.pem'
        client_pem = client_pem if client_pem else 'client.pem'
        client_key = client_key if client_key else 'client.key'

        if os.path.isfile(ca_pem):
            self.url_type = 'https'
            self.session.cert = (client_pem, client_key)
            self.session.verify = ca_pem

    def tags(self, args=dict()):
        for i in range(len(self.servers)):
            srv = '{}://{}'.format(self.url_type, random.choice(self.servers))

            try:
                r = self.session.get('{}'.format(srv), params=args)
                if 200 == r.status_code:
                    return extract_response(r)
            except Exception:
                pass

    def tail(self, seq, tags=dict()):
        while True:
            srv = '{}://{}'.format(self.url_type, random.choice(self.servers))
            try:
                res = dict(server=srv, seq=seq)
                r = self.session.get('{}/{}'.format(srv, seq), params=tags)
                if 200 != r.status_code:
                    raise Exception('http_response : {}'.format(r.status_code))

                res = extract_response(r)
                yield res

                seq = int(res['seq']) + 1
            except Exception as e:
                res.update(dict(exception=str(e)))
                yield res

    def append(self, blob, tags=dict()):
        for i in range(len(self.servers)):
            srv = '{}://{}'.format(self.url_type, random.choice(self.servers))

            try:
                r = self.session.post(srv, params=tags, data=blob)
                if 200 == r.status_code:
                    return extract_response(r)
            except Exception:
                pass

    def put(self, key, blob):
        for i in range(len(self.servers)):
            srv = '{}://{}'.format(self.url_type, random.choice(self.servers))
            key = key.strip('/')

            try:
                r = self.session.put('{}//{}'.format(srv, key), data=blob)
                if 204 == r.status_code:
                    return extract_response(r)
            except Exception:
                pass

    def get(self, key):
        for i in range(len(self.servers)):
            srv = '{}://{}'.format(self.url_type, random.choice(self.servers))
            key = key.strip('/')

            try:
                r = self.session.get('{}//{}'.format(srv, key))
                if 200 == r.status_code:
                    return extract_response(r)
            except Exception:
                pass
