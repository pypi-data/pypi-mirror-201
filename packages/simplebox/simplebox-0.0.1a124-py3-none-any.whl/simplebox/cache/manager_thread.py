#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
from threading import RLock
from typing import Any, Optional, Dict

from . import Cache
from .manager import _Singleton
from ..classes import StaticClass


class _ManagerThread(metaclass=_Singleton):
    _lock = RLock()

    def __init__(self):
        self.__manager_thread = {}

    def remove(self, key):
        with self._lock:
            if self.has_cache(key):
                del self.__get_thread_cache_map[key]

    def put(self, key: Any, data: Any = None, duration: int = -1):
        with self._lock:
            cache: Cache = Cache(data, duration)
            self.__get_thread_cache_map[key] = cache

    def get_cache(self, key: Any) -> Optional[Cache]:
        with self._lock:
            cache: Cache = self.__get_thread_cache_map.get(key)
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
        return key in self.__get_thread_cache_map

    def is_expired(self, key: Any) -> bool:
        cache: Cache = self.__get_thread_cache_map.get(key)
        if cache:
            if cache.is_expired:
                self.remove(key)
                return True
            else:
                return False
        return True

    @property
    def __get_thread_cache_map(self) -> Dict[Any, Cache]:
        t_id = threading.current_thread().ident
        thread_manager = self.__manager_thread.get(t_id)
        if thread_manager is None:
            thread_manager = {}
            self.__manager_thread[t_id] = thread_manager
        return thread_manager


class CacheManagerThread(metaclass=StaticClass):
    """
    A simple cache manager.
    Cache is stored on a per-thread basis.
    """
    _manager: _ManagerThread = _ManagerThread()

    @staticmethod
    def remove(key: Any):
        """
        remove cache
        """
        return CacheManagerThread._manager.remove(key)

    @staticmethod
    def get_cache(key: Any) -> Optional[Cache]:
        """
        get contain origin data's cache object
        """
        return CacheManagerThread._manager.get_cache(key)

    @staticmethod
    def get_data(key: Any, default: Any = None) -> Any:
        """
        get origin data

        """
        return CacheManagerThread._manager.get_data(key, default)

    @staticmethod
    def put(key: Any, data: Any = None, duration: int = -1):
        """
        add cache
        """
        return CacheManagerThread._manager.put(key, data, duration)

    @staticmethod
    def has_cache(key: Any) -> bool:
        """
        check has cache
        """
        return CacheManagerThread._manager.has_cache(key)

    @staticmethod
    def is_expired(key: Any) -> bool:
        """
        check expired.
        if expiration, returns False, and clears the cache
        """
        return CacheManagerThread._manager.is_expired(key)


__all__ = [CacheManagerThread]
