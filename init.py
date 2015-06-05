#!/usr/bin/env python
# encoding: utf-8

import sys

from os.path import dirname, abspath
PROJECT_PATH = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)

from bson.objectid import ObjectId

from consts import (REDIS_KEY_LAST_OID, REDIS_KEY_TO_BE_MERGED,
                    REDIS_KEY_TO_BE_EXPORTED, REDIS_KEY_EXPORT_LAST_OID,
                    REDIS_KEY_COMPLETE_SELECTOR_LOCK, REDIS_KEY_DISPATCHER_LOCK)
from common.redis_client import r
from common.mongo import db


def main(arg):
    n = 1000 if len(arg) < 2 else int(arg[1])

    cross_data = {
        'collection1': [gen1(x, x, bool(x % 2)) for x in range(1, n)],
        'collection2': [gen2(x, x, bool(x % 2)) for x in range(1, n)],
    }

    nocross_data = {
        'collection1': [gen1(x, x-10, bool(x % 2)) for x in range(n+1, 2*n)],
        'collection2': [gen2(x, x+10, bool(x % 2)) for x in range(n+1, 2*n)],
    }

    db.collection1.remove({})
    db.collection2.remove({})
    for collection_name, d in cross_data.iteritems():
        c = db[collection_name]
        print collection_name
        for i in d:
            print i
            c.insert(i)

    for collection_name, d in nocross_data.iteritems():
        c = db[collection_name]
        print collection_name
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
    r.delete(REDIS_KEY_COMPLETE_SELECTOR_LOCK)
    r.delete(REDIS_KEY_DISPATCHER_LOCK)
    print 'redis cleared.'


def gen1(n, c2n, completed=False):
    r = {
        '_id': ObjectId('1{0:023d}'.format(n)),
        'collection2_id': ObjectId('2{0:023d}'.format(c2n)),
        'data': str(n),
    }
    if completed:
        r['completed'] = True

    return r


def gen2(n, c1n, completed=False):
    r = {
        '_id': ObjectId('2{0:023d}'.format(n)),
        'collection1_id': ObjectId('1{0:023d}'.format(c1n)),
        'data': str(n),
    }
    if completed:
        r['completed'] = True

    return r


if __name__ == '__main__':
    main(sys.argv)
