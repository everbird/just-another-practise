#!/usr/bin/env python
# encoding: utf-8


from pymongo import MongoClient

HOST = 'localhost'
PORT = 27017
DB = 'homework'

client = MongoClient('mongodb://{host}:{port}/'.format(
    host=HOST,
    port=PORT
))

db = client.homework
