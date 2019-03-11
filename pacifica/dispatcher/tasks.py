#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The Celery tasks module."""
from os import getenv
from celery import Celery, Task
from pacifica.dispatcher import Dispatcher
from .orm import DispatcherModel

CELERY_APP = Celery(
    'notifications',
    broker=getenv('BROKER_URL', 'pyamqp://'),
    backend=getenv('BACKEND_URL', 'rpc://')
)


# pylint: disable=too-few-public-methods
# pylint: disable=abstract-method
class DispatcherTask(Task):
    """Dispatcher Task Class."""

    def on_success(self, retval, task_id, args, kwargs):
        """On success save the return value to DB."""
        super(DispatcherTask, self).on_success(retval, task_id, args, kwargs)
        new_task = DispatcherModel(
            uuid=task_id,
            value=retval
        )
        DispatcherModel.connect()
        with DispatcherModel.atomic():
            new_task.save(force_insert=True)
        DispatcherModel.close()


@CELERY_APP.task(base=DispatcherTask)
def dispatcher_task(method_str, *numbers):
    """Get all the events and see which match."""
    numbers_copy = []
    for value in numbers:
        try:
            numbers_copy.append(int(value))
        except ValueError:
            numbers_copy.append(value)
    return getattr(Dispatcher, method_str)(*numbers_copy)
