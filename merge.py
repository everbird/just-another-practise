#!/usr/bin/env python
# encoding: utf-8


from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://localhost:27017/')
db = client.homework
c1 = db.collection1
c2 = db.collection2
c3 = db.collection3

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

REDIS_KEY_TO_BE_MERGED = 'homework/to_be_merged'
TIMEOUT = 5


def main():
    while True:
        ret = r.brpop(REDIS_KEY_TO_BE_MERGED, TIMEOUT)
        if ret is None:
            print 'No work to do.'
            break

        _, data = ret
        oid1 = data[:24]
        oid2 = data[24:]
        print oid1, oid2
        item1 = c1.find_one({'_id': ObjectId(oid1)})
        item2 = c2.find_one({'_id': ObjectId(oid2)})
        print item1, item2
        if item1 and item2:
            rs = c3.insert({
                'item1': item1,
                'item2': item2
            })
            print rs, 'inserted.'


if __name__ == '__main__':
    main()
