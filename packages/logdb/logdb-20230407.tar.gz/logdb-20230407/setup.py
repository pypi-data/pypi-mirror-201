import time
import glob
from distutils.core import setup

setup(
  name = 'logdb',
  packages = ['logdb'],
  scripts=['bin/logdb-ca'],
  version = time.strftime('%Y%m%d'),
  description = 'A simple Queue and DB - with append/tail and get/put operations over HTTPS.',
  long_description = 'Uses Paxos for replication and mTLS for auth. Leaderless and highly available.',
  author = 'Bhupendra Singh',
  author_email = 'bhsingh@gmail.com',
  url = 'https://github.com/magicray/logdb',
  keywords = ['queue', 'paxos', 'pubsub', 'pub', 'sub', 'kv', 'key', 'value', 'mtls']
)
