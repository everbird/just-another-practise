#!/usr/bin/env python
# encoding: utf-8

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/1')
app.config_from_object('celeryconfig')


@app.task
def scheduler():
    import dispatcher
    dispatcher.main()


@app.task
def complete_selector():
    import to_export
    to_export.main((None, 1))
    to_export.main((None, 2))
