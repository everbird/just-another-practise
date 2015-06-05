#!/usr/bin/env python
# encoding: utf-8


from pymongo import MongoClient
from bson.objectid import ObjectId

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

REDIS_KEY_LAST_OID = 'homework/last_oid'
REDIS_KEY_TO_BE_MERGED = 'homework/to_be_merged'
REDIS_KEY_EXPORT_LAST_OID = 'homework/to_export/collection{}/last_oid'
REDIS_KEY_TO_BE_EXPORTED = 'homework/to_export/collection/{}/to_be_exported'


def main():
    client = MongoClient('mongodb://localhost:10001/')
    db = client.homework
    for collection_name, d in data.iteritems():
        c = db[collection_name]

        print collection_name

        c.remove({})
        for i in d:
            print i
            c.insert(i)

    db.collection3.remove({})
    clear_redis()


def clear_redis():
    r.delete(REDIS_KEY_LAST_OID)
    r.delete(REDIS_KEY_TO_BE_MERGED)
    r.delete(REDIS_KEY_TO_BE_EXPORTED.format(1))
    r.delete(REDIS_KEY_TO_BE_EXPORTED.format(2))
    r.delete(REDIS_KEY_EXPORT_LAST_OID.format(1))
    r.delete(REDIS_KEY_EXPORT_LAST_OID.format(2))
    print 'redis cleared.'


data = {
    'collection1': [
        {
            '_id': ObjectId('100000000000000000000001'),
            'collection2_id': ObjectId('200000000000000000000001'),
            'data': '1',
            'completed': True
        },
        {
            '_id': ObjectId('100000000000000000000002'),
            'collection2_id': ObjectId('200000000000000000000002'),
            'data': '2'
        },
        {
            '_id': ObjectId('100000000000000000000003'),
            'collection2_id': ObjectId('200000000000000000000004'),
            'data': '3'
        },
        {
            '_id': ObjectId('100000000000000000000005'),
            'collection2_id': ObjectId('200000000000000000000005'),
            'data': '3'
        },
        {
            '_id': ObjectId('100000000000000000000006'),
            'collection2_id': ObjectId('200000000000000000000006'),
            'data': '3'
        },
    ],
    'collection2': [
        {
            '_id': ObjectId('200000000000000000000001'),
            'collection2_id': ObjectId('100000000000000000000001'),
            'data': 'a',
            'completed': True
        },
        {
            '_id': ObjectId('200000000000000000000002'),
            'collection2_id': ObjectId('100000000000000000000002'),
            'data': 'b'
        },
        {
            '_id': ObjectId('200000000000000000000003'),
            'collection2_id': ObjectId('100000000000000000000004'),
            'data': 'c',
            'completed': True
        },
        {
            '_id': ObjectId('200000000000000000000005'),
            'collection2_id': ObjectId('100000000000000000000005'),
            'data': 'c',
            'completed': True
        },
        {
            '_id': ObjectId('200000000000000000000006'),
            'collection2_id': ObjectId('100000000000000000000006'),
            'data': 'c',
            'completed': True
        },
    ]
}


if __name__ == '__main__':
    main()
