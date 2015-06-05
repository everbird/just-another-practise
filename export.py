#!/usr/bin/env python
# encoding: utf-8


import sys
import subprocess
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client.homework

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

REDIS_KEY_TO_BE_EXPORTED = 'homework/to_export/collection/{}/to_be_exported'


def main(arg):
    n = arg[1]
    path = arg[2]
    limit = 5
    oids = []
    while True:
        _, oid = r.brpop(REDIS_KEY_TO_BE_EXPORTED.format(n))
        oids.append(oid)
        if len(oids) >= limit:
            with open(path, 'a') as f:
                content = mongoexport(n, oids)
                f.write(content)
                oids = []
            print content,


def mongoexport(num, ids):
    cmd = 'mongoexport --host {host} --port {port} --db {db} --collection {collection}'.format(
        host='localhost',
        port=27017,
        db='homework',
        collection='collection%s' % num,
    )
    inputs = cmd.split()
    inputs.append('-q')
    oids = ','.join(['{"$oid": "%s"}' % x for x in ids])
    inputs.append('{_id: {$in: [%s]}}' % oids)
    p = subprocess.Popen(inputs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r, _ = p.communicate()
    return r

if __name__ == '__main__':
    main(sys.argv)
