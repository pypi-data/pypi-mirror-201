#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from pathlib import Path
from threading import RLock
from typing import Union

_RESOURCES = "resources"


class __PropertyConfig(object):
    """
    Property   source   config
    """

    __lock__ = RLock()
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls.__lock__:
                if not hasattr(cls, "_instance"):
                    cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__resources_dir: Path = Path.cwd().joinpath(_RESOURCES)

    @property
    def resources(self) -> Path:
        """
        get properties file dir.
        It's not that the directory where the python file you run is called the working directory,
        but that when you run the script on the command line, the command line displays the directory you are in.
        """
        return self.__resources_dir

    @resources.setter
    def resources(self, value: Union[Path, str, os.PathLike]):
        """
        set resources dir.
        """
        if issubclass(type(value), (Path, str, os.PathLike)):
            self.__resources_dir = Path(value)
        else:
            raise TypeError(f"Excepted type is str, bytes, os.PathLike, got {type(value).__name__}")


PropertyConfig = __PropertyConfig()

__all__ = [PropertyConfig]
