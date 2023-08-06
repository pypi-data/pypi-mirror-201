#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from typing import Any


class Cache(object):
    """
    Cached atomic objects
    """

    def __init__(self, data: Any, duration: int = -1):
        self.__data: Any = data  # cache data
        self.__duration: int = duration  # storage time(millisecond), if -1 will never expires
        self.__timestamp: int = int(
            round(time.time() * 1000))  # the timestamp at the time the deposit operation was performed

    @property
    def data(self) -> Any:
        return self.__data

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def timestamp(self) -> int:
        return self.__timestamp

    @property
    def is_expired(self) -> bool:
        """
        Check whether it expires.
        """
        if self.__duration == -1:
            return False
        now = int(round(time.time() * 1000))
        return now - self.__timestamp > self.__duration


__all__ = [Cache]
