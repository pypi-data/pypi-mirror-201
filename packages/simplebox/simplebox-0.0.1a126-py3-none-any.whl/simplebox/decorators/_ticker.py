#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
from typing import Callable, Tuple, Dict, Any

from ..decorators._process import _do
from ..scheduler import Ticker


def ticker_apply(interval: int = 1, num: int = 1):
    """
    A simple scheduled sync task trigger.
    The task should not be expected to have a return.
    :param interval: task execution interval
    :param num: task run times, less than 0 will always be executed.
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"interval": interval, "num": num, "stacklevel": 7}
            return _do(func=func, decorator_name=ticker_apply.__name__, args=args, kwargs=kwargs, opts=opts)
        return __wrapper
    return __inner


def ticker_apply_async(interval: int = 1, num: int = 1):
    """
    A simple scheduled async task trigger.
    The task should not be expected to have a return.
    :param interval: task execution interval
    :param num: task run times, less than 0 will always be executed.
    """
    def __inner(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            opts = {"interval": interval, "num": num, "stacklevel": 7}
            return _do(func=func, decorator_name=ticker_apply_async.__name__, args=args, kwargs=kwargs, opts=opts)
        return __wrapper
    return __inner


def __do_ticker_apply(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None) -> Any:
    interval = opts.get("interval")
    num = opts.get("num")
    args_ = args or ()
    kwargs_ = kwargs or {}
    Ticker(interval).apply(num, func, args_, kwargs_)


def __do_ticker_apply_async(func: Callable, args: Tuple = None, kwargs: Dict = None, opts: Dict = None) -> Any:
    interval = opts.get("interval")
    num = opts.get("num")
    args_ = args or ()
    kwargs_ = kwargs or {}
    Ticker(interval).apply_async(num, func, args_, kwargs_)


__all__ = [ticker_apply, ticker_apply_async]
