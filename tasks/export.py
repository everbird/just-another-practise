#!/usr/bin/env python
# encoding: utf-8


import sys
import subprocess
from os.path import dirname, abspath
PROJECT_PATH = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)

from pymongo import MongoClient

from common.redis_client import r


client = MongoClient('mongodb://localhost:27017/')
db = client.homework

REDIS_KEY_TO_BE_EXPORTED = 'homework/to_export/collection/{}/to_be_exported'
TIMEOUT = 5


def main(arg):
    n = arg[1]
    path = arg[2]
    limit = 5
    oids = []
    print 'collection#:', n, 'path:', path
    while True:
        timeout = False
        ret = r.brpop(REDIS_KEY_TO_BE_EXPORTED.format(n), TIMEOUT)
        if ret is None:
            timeout = True
        else:
            _, oid = ret
            oids.append(oid)

        if not oids and timeout:
            print 'No work to export.'
            break

        # Export for mutilti ids one time. If no id in queue, start export
        # immediately
        if len(oids) >= limit or timeout:
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
