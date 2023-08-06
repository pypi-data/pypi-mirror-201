#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
from typing import Callable, Tuple, Dict

from psutil import cpu_count

from ..decorators._process import _do
from ..scheduler import SchedulerSync, SchedulerAsync, SchedulerSyncProcess, SchedulerAsyncProcess, SchedulerAsyncIO, \
    SchedulerGevent

_THREAD_POOLS = 20
_PROCESS_POOLS = int(cpu_count() / 2) or 1


def scheduler_sync(cron, pools: int = _THREAD_POOLS, timezone=None, jitter=None):
    """
    SchedulerSync's decorator mode, reference SchedulerSync.
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"cron": cron, "pools": pools, "timezone": timezone, "jitter": jitter, "stacklevel": 7}
            return _do(func=func, decorator_name=scheduler_sync.__name__, args=args, kwargs=kwargs, opts=opts)

        return __wrapper

    return __inner


def scheduler_async(cron, pools: int = _THREAD_POOLS, timezone=None, jitter=None):
    """
    SchedulerAsync's decorator mode, reference SchedulerAsync.
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"cron": cron, "pools": pools, "timezone": timezone, "jitter": jitter, "stacklevel": 7}
            return _do(func=func, decorator_name=scheduler_async.__name__, args=args, kwargs=kwargs, opts=opts)

        return __wrapper

    return __inner


def scheduler_sync_process(cron, pools: int = _THREAD_POOLS, timezone=None, jitter=None):
    """
    SchedulerSyncProcess's decorator mode, reference SchedulerSyncProcess.
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"cron": cron, "pools": pools, "timezone": timezone, "jitter": jitter, "stacklevel": 7}
            return _do(func=func, decorator_name=scheduler_sync_process.__name__, args=args, kwargs=kwargs, opts=opts)

        return __wrapper

    return __inner


def scheduler_async_process(cron, pools: int = _THREAD_POOLS, timezone=None, jitter=None):
    """
    SchedulerAsyncProcess's decorator mode, reference SchedulerAsyncProcess.
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"cron": cron, "pools": pools, "timezone": timezone, "jitter": jitter, "stacklevel": 7}
            return _do(func=func, decorator_name=scheduler_async_process.__name__, args=args, kwargs=kwargs, opts=opts)

        return __wrapper

    return __inner


def scheduler_asyncio(cron, timezone=None, jitter=None):
    """
    SchedulerAsyncIO's decorator mode, reference SchedulerAsyncIO.
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"cron": cron, "timezone": timezone, "jitter": jitter, "stacklevel": 7}
            return _do(func=func, decorator_name=scheduler_async_process.__name__, args=args, kwargs=kwargs, opts=opts)

        return __wrapper

    return __inner


def scheduler_gevent(cron, timezone=None, jitter=None):
    """
    SchedulerGevent's decorator mode, reference SchedulerGevent.
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"cron": cron,  "timezone": timezone, "jitter": jitter, "stacklevel": 7}
            return _do(func=func, decorator_name=scheduler_async_process.__name__, args=args, kwargs=kwargs, opts=opts)

        return __wrapper

    return __inner


def __do_scheduler_sync(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None):
    cron = opts.get("cron")
    pools = opts.get("pools")
    timezone = opts.get("timezone")
    jitter = opts.get("jitter")
    SchedulerSync(cron, pools, timezone, jitter).run(func, args, kwargs)


def __do_scheduler_async(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None):
    cron = opts.get("cron")
    pools = opts.get("pools")
    timezone = opts.get("timezone")
    jitter = opts.get("jitter")
    SchedulerAsync(cron, pools, timezone, jitter).run(func, args, kwargs)


def __do_scheduler_sync_process(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None):
    cron = opts.get("cron")
    pools = opts.get("pools")
    timezone = opts.get("timezone")
    jitter = opts.get("jitter")
    SchedulerSyncProcess(cron, pools, timezone, jitter).run(func, args, kwargs)


def __do_scheduler_async_process(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None):
    cron = opts.get("cron")
    pools = opts.get("pools")
    timezone = opts.get("timezone")
    jitter = opts.get("jitter")
    SchedulerAsyncProcess(cron, pools, timezone, jitter).run(func, args, kwargs)


def __do_scheduler_asyncio(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None):
    cron = opts.get("cron")
    timezone = opts.get("timezone")
    jitter = opts.get("jitter")
    SchedulerAsyncIO(cron, timezone, jitter).run(func, args, kwargs)


def __do_scheduler_gevent(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None):
    cron = opts.get("cron")
    timezone = opts.get("timezone")
    jitter = opts.get("jitter")
    SchedulerGevent(cron, timezone, jitter).run(func, args, kwargs)


__all__ = [scheduler_sync, scheduler_async, scheduler_sync_process, scheduler_async_process]
