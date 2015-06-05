#!/usr/bin/env python
# encoding: utf-8


import sys

from os.path import dirname, abspath
PROJECT_PATH = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)

from functools import wraps

from consts import LOCK_EXPIRE
from common.redis_client import r


def check_lock(key):
    def deco(f):
        @wraps(f)
        def _(*args, **kwargs):
            if not r.get(key):
                r.set(key, 'true', ex=LOCK_EXPIRE)
                ret = f(*args, **kwargs)
                return ret
        return _
    return deco
