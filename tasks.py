#!/usr/bin/env python
# encoding: utf-8

from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/1')
app.config_from_object('celeryconfig')


@app.task
def add(x, y):
    return x + y
