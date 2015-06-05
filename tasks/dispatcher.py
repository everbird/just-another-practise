#!/usr/bin/env python
# encoding: utf-8

import sys

from os.path import dirname, abspath
PROJECT_PATH = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)

from bson.objectid import ObjectId

from consts import (REDIS_KEY_LAST_OID, REDIS_KEY_TO_BE_MERGED,
                    REDIS_KEY_DISPATCHER_LOCK)
from common.redis_client import r
from common.mongo import db
from common.lock import check_lock


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

        new_last_oid = item1['_id']

    print last_oid, '->', new_last_oid

    r.set(REDIS_KEY_LAST_OID, new_last_oid)

if __name__ == '__main__':
    main()
