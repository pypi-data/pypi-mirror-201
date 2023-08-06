import sys
import json
import logdb


def main():
    client = logdb.Client(sys.argv[1].split(','))

    args = dict()
    for argv in sys.argv[2:]:
        k, v = argv.split('=')
        args[k] = v

    result = client.tags(args)
    if not result:
        exit(1)

    blob = result.pop('blob', b'')
    sys.stderr.write(json.dumps(result, indent=4, sort_keys=True) + '\n\n')
    print(blob.decode())


if '__main__' == __name__:
    main()
