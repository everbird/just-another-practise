#!/usr/bin/env python
# encoding: utf-8


import redis

HOST = 'localhost'
PORT = 6379
DB = 0

r = redis.StrictRedis(
    host=HOST,
    port=PORT,
    db=DB
)
