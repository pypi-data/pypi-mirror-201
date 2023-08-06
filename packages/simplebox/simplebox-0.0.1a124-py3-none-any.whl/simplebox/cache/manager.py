#!/usr/bin/env python
# -*- coding:utf-8 -*-
from threading import RLock
from typing import Any, Optional

from . import Cache
from ..classes import StaticClass


class _Singleton(type):
    """
    singletons
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _Manager(metaclass=_Singleton):
    _lock = RLock()

    def __init__(self):
        self.__manager = {}

    def remove(self, key):
        with self._lock:
            if self.has_cache(key):
                del self.__manager[key]

    def put(self, key: Any, data: Any = None, duration: int = -1):
        with self._lock:
            cache: Cache = Cache(data, duration)
            self.__manager[key] = cache

    def get_cache(self, key: Any) -> Optional[Cache]:
        with self._lock:
            cache: Cache = self.__manager.get(key)
            if cache:
                if cache.is_expired:
                    self.remove(key)
                    return None
                else:
                    return cache
            return None

    def get_data(self, key: Any, default: Any = None) -> Any:
        cache: Cache = self.get_cache(key)
        if cache:
            return cache.data
        else:
            return default

    def has_cache(self, key: Any) -> bool:
        return key in self.__manager

    def is_expired(self, key: Any) -> bool:
        cache: Cache = self.__manager.get(key)
        if cache:
            if cache.is_expired:
                self.remove(key)
                return True
            else:
                return False
        return True


class CacheManager(metaclass=StaticClass):
    """
    A simple cache manager
    """
    _manager: _Manager = _Manager()

    @staticmethod
    def remove(key: Any):
        """
        remove cache
        """
        return CacheManager._manager.remove(key)

    @staticmethod
    def get_cache(key: Any) -> Optional[Cache]:
        """
        get contain origin data's cache object
        """
        return CacheManager._manager.get_cache(key)

    @staticmethod
    def get_data(key: Any, default: Any = None) -> Any:
        """
        get origin data

        """
        return CacheManager._manager.get_data(key, default)

    @staticmethod
    def put(key: Any, data: Any = None, duration: int = -1):
        """
        add cache
        """
        return CacheManager._manager.put(key, data, duration)

    @staticmethod
    def has_cache(key: Any) -> bool:
        """
        check has cache
        """
        return CacheManager._manager.has_cache(key)

    @staticmethod
    def is_expired(key: Any) -> bool:
        """
        check expired.
        if expiration, returns False, and clears the cache
        """
        return CacheManager._manager.is_expired(key)


__all__ = [CacheManager]
