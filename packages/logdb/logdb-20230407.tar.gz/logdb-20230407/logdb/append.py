import sys
import json
import logdb


def main():
    client = logdb.Client(sys.argv[1].split(','))

    tags = dict()
    for argv in sys.argv[2:]:
        k, v = argv.split('=')
        tags[k] = v

    result = client.append(sys.stdin.read(), tags)
    if not result:
        exit(1)

    result.pop('blob')
    sys.stderr.write(json.dumps(result, indent=4, sort_keys=True) + '\n')


if '__main__' == __name__:
    main()
