#!/usr/bin/env python
# encoding: utf-8


import sys

from os.path import dirname, abspath
PROJECT_PATH = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)

from bson.objectid import ObjectId

from consts import (REDIS_KEY_TO_BE_EXPORTED, REDIS_KEY_EXPORT_LAST_OID,
                    REDIS_KEY_COMPLETE_SELECTOR_LOCK)

from common.redis_client import r
from common.mongo import db
from common.lock import check_lock


@check_lock(REDIS_KEY_COMPLETE_SELECTOR_LOCK)
def main(args):
    print 'in'
    n = args[1]
    c = db['collection{}'.format(n)]
    last_oid = r.get(REDIS_KEY_EXPORT_LAST_OID.format(n)) or '0' * 24
    new_last_oid = last_oid
    for i in c.find({'_id': {'$gt': ObjectId(last_oid)}}):
        if i.get('completed'):
            r.lpush(REDIS_KEY_TO_BE_EXPORTED.format(n), i['_id'])

        new_last_oid = i['_id']

    print last_oid, '->', new_last_oid

    r.set(REDIS_KEY_EXPORT_LAST_OID.format(n), new_last_oid)

if __name__ == '__main__':
    main(sys.argv)
