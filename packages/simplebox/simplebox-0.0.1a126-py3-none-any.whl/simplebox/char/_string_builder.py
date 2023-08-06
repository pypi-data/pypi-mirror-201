#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Callable, Optional, Iterable

from . import String
from ..collection import Array
from ..generic import T


class StringBuilder(Array[T]):
    """
    Enhanced string connector.
    It provides functions such as connectors, start characters, end characters, and custom string callback functions.
    """

    def __init__(self, sep: Optional[str] = "", start: Optional[str] = "", end: Optional[str] = ""):
        """
        :param sep: A connector for multiple elements when converted to a string
        :param start: After conversion to a string, the beginning of the string
        :param end: The end of the string after conversion to a string
        """
        self.__append = super().append
        self.__sep = str(sep)
        self.__start = str(start)
        self.__end = str(end)
        super(StringBuilder, self).__init__(list())

    def __str__(self) -> String:
        return self.string()

    def string(self, call_has_index: Callable[[int, T], str] = None, call_no_index: Callable[[T], str] = None) \
            -> String:
        """
        Convert StringBuilder to string
        Provides two different callback functions for element handling,
        if you do not provide a processing callback function, it will be directly concatenated
        :param call_has_index: Pass in the element subscript and the element itself
                like:
                    s = StringBuilder()
                    s.append("a").append("b").append("c")
                    print(s.string(call_has_index=lambda i, v: f"{i}{v}"))  => 0a1b2c
        :param call_no_index: Only the element is passed in
                like:
                    s = StringBuilder()
                    s.append("a").append("b").append("c")
                    print(s..string(call_no_index=lambda v: f"value={v}")) => value=avalue=bvalue=c
        :no params:
                like:
                    s = StringBuilder()
                    s.append("a").append("b").append("c")
                    print(s..string() => 123
        """
        content = self.__start
        if issubclass(type(call_has_index), Callable):
            content += _join((call_has_index(i, v) for i, v in enumerate(self)), self.__sep)
        elif issubclass(type(call_no_index), Callable):
            content += _join((call_no_index(v) for v in self), self.__sep)
        else:
            content += _join(self, self.__sep)
        content += self.__end
        return String(content)

    def append(self, __object: T) -> 'StringBuilder':
        """
        Add a character element
        """
        self.__append(__object)
        return self


def _join(iterable: Iterable, connector: str = "") -> String:
    """
    You can receive elements for any type of iteration object for join operations.
    """
    return String(connector.join((str(i) for i in iterable)))


__all__ = [StringBuilder]
