#!/usr/bin/env python
# encoding: utf-8

import os
from celery import Celery
from config import PROJECT_PATH

app = Celery('tasks', broker='redis://localhost:6379/1')
app.config_from_object('celeryconfig')


@app.task
def scheduler():
    import dispatcher
    dispatcher.main()


@app.task
def to_export(collection_num):
    import to_export
    to_export.main((None, collection_num))


@app.task
def complete_selector():
    to_export.delay(1)
    to_export.delay(2)


@app.task
def merge_worker():
    import merge
    merge.main()


@app.task
def start_merge_workers():
    for i in range(5):
        merge_worker.delay()


@app.task
def export_worker(collection_num, shard):
    import export
    export.main((None, collection_num,
                 os.path.join(
                     PROJECT_PATH,
                     'data',
                     'export',
                     '{}-{}'.format(collection_num, shard))))


@app.task
def start_export_workers():
    for i in range(1, 4):
        export_worker.delay(1, i)

    for i in range(1, 4):
        export_worker.delay(2, i)
