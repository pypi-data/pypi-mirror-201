import sys
import time
import json
import logdb
import hashlib


def main():
    client = logdb.Client(sys.argv[1].split(','))

    tags = dict()
    for argv in sys.argv[3:]:
        k, v = argv.split('=')
        tags[k] = v

    chksum = ''
    for r in client.tail(int(sys.argv[2]), tags):
        if 'blob' in r:
            blob = r.pop('blob', b'')
            if blob:
                r['blob_hash'] = hashlib.md5(blob).hexdigest()
                chksum += r['blob_hash']
                r['log_hash'] = hashlib.md5(chksum.encode()).hexdigest()
            sys.stderr.write(json.dumps(r, indent=4, sort_keys=True) + '\n')
        else:
            time.sleep(1)


if '__main__' == __name__:
    main()
