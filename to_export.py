#!/usr/bin/env python
# encoding: utf-8


import sys

from functools import wraps
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://localhost:27017/')
db = client.homework

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

REDIS_KEY_EXPORT_LAST_OID = 'homework/to_export/collection{}/last_oid'
REDIS_KEY_TO_BE_EXPORTED = 'homework/to_export/collection/{}/to_be_exported'

REDIS_KEY_COMPLETE_SELECTOR_LOCK = 'homework/complete_selector/lock'
LOCK_EXPIRE = 60


def check_lock(key):
    def deco(f):
        @wraps(f)
        def _(*args, **kwargs):
            if not r.get(key):
                r.set(key, 'true', LOCK_EXPIRE)
                ret = f(*args, **kwargs)
                return ret
        return _
    return deco


@check_lock(REDIS_KEY_COMPLETE_SELECTOR_LOCK)
def main(args):
    n = args[1]
    c = db['collection{}'.format(n)]
    last_oid = r.get(REDIS_KEY_EXPORT_LAST_OID.format(n)) or '0' * 24
    new_last_oid = last_oid
    for i in c.find({'_id': {'$gt': ObjectId(last_oid)}}):
        if i.get('completed'):
            r.lpush(REDIS_KEY_TO_BE_EXPORTED.format(n), i['_id'])

        new_last_oid = i['_id']

    print last_oid, '->', new_last_oid

    r.set(REDIS_KEY_EXPORT_LAST_OID, new_last_oid)

if __name__ == '__main__':
    main(sys.argv)
