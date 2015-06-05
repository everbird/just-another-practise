#!/usr/bin/env python
# encoding: utf-8

from functools import wraps
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://localhost:27017/')
db = client.homework

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

REDIS_KEY_LAST_OID = 'homework/last_oid'
REDIS_KEY_TO_BE_MERGED = 'homework/to_be_merged'
REDIS_KEY_TO_BE_EXPORTED = 'homework/collection/{}/to_be_exported'

REDIS_KEY_DISPATCHER_LOCK = 'homework/dispatcher/lock'
LOCK_EXPIRE = 15


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


@check_lock(REDIS_KEY_DISPATCHER_LOCK)
def main():
    c1 = db.collection1
    c2 = db.collection2
    last_oid = r.get(REDIS_KEY_LAST_OID) or '0' * 24
    new_last_oid = last_oid
    for item1 in c1.find({'_id': {'$gt': ObjectId(last_oid)}}):
        item2 = c2.find_one({'_id': item1['collection2_id']})
        if item2:
            print 'dispatching...', item1['_id'], item2['_id']
            r.lpush(REDIS_KEY_TO_BE_MERGED,
                    '{}{}'.format(item1['_id'], item2['_id']))

        if item1 and item1.get('completed'):
            r.lpush(REDIS_KEY_TO_BE_EXPORTED.format(1), item1['_id'])

        if item2 and item2.get('completed'):
            r.lpush(REDIS_KEY_TO_BE_EXPORTED.format(2), item2['_id'])

        new_last_oid = item1['_id']

    print last_oid, '->', new_last_oid

    r.set(REDIS_KEY_LAST_OID, new_last_oid)

if __name__ == '__main__':
    main()
