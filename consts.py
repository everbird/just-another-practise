#!/usr/bin/env python
# encoding: utf-8


REDIS_KEY_LAST_OID = 'homework/last_oid'
REDIS_KEY_TO_BE_MERGED = 'homework/to_be_merged'
REDIS_KEY_EXPORT_LAST_OID = 'homework/to_export/collection{}/last_oid'
REDIS_KEY_TO_BE_EXPORTED = 'homework/to_export/collection/{}/to_be_exported'
REDIS_KEY_COMPLETE_SELECTOR_LOCK = 'homework/complete_selector/lock'
REDIS_KEY_DISPATCHER_LOCK = 'homework/dispatcher/lock'


LOCK_EXPIRE = 15

BRPOP_TIMEOUT = 5
