#!/usr/bin/env python
# -*- coding:utf-8 -*-
from threading import RLock
from typing import Any


class _DecoratorsCache(object):
    __cache = {}
    __lock = RLock()
    __instance = None

    def __new__(cls, *args, **kwargs):
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = object.__new__(cls)
        return cls.__instance

    @staticmethod
    def get(key: Any, default: Any = None) -> Any:
        """
        get origin data

        """
        with _DecoratorsCache.__lock:
            return _DecoratorsCache.__cache.get(key, default)

    @staticmethod
    def put(key: Any, data: Any = None):
        """
        add cache
        """
        with _DecoratorsCache.__lock:
            _DecoratorsCache.__cache[key] = data

    @staticmethod
    def has_cache(key: Any) -> bool:
        """
        check has cache
        """
        with _DecoratorsCache.__lock:
            return key in _DecoratorsCache.__cache
