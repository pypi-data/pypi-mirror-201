#!/usr/bin/env python
# -*- coding:utf-8 -*-
import builtins
import inspect
import os
import pickle
import platform
from locale import getpreferredencoding
from pathlib import Path
from subprocess import Popen, PIPE
from sys import executable
from tempfile import gettempdir
from typing import Callable, Iterable, Dict

from ..char import StringBuilder, String
from ..config import LogConfig
from ..log import LoggerFactory
from ..utils import ObjectsUtils, StringUtils
from ._run import _Runner

_logger = LoggerFactory.get_logger("backend")

_inner_type = dir(builtins)

_run_module_name = _Runner.__name__


class _Backend(object):
    """
    Create a new process and then run it in background mode
    """

    def __init__(self, func: Callable, args: Iterable = None, kwargs: Dict = None, log_path: str or Path = None):
        self.__all_args = (args or [], kwargs or {})
        self.__message_builder = StringBuilder()
        self.__message_builder.append(f"Backend run [{platform.system()}]: ")
        if not issubclass(type(func), Callable):
            raise TypeError(f"expected is function, got a {type(func).__name__}")
        self.__func_name = func.__name__
        self.__func = func
        if self.__func_name == "<lambda>":
            raise TypeError("cannot be a lambda function")
        self.__log_path = None
        if log_path and issubclass(type(log_path), (str, Path)):
            p = Path(log_path)
            if not p.is_absolute():
                self.__log_path = LogConfig.dir.joinpath(log_path)
            else:
                self.__log_path = p
        self.__frame = inspect.stack()[2]
        self.__run_path = Path(self.__frame[1]).parent
        self.__module_name = Path(self.__frame[1]).stem
        # When find for processes, you can filter by filtering the keywords in commandline (flag here).
        self.__flag = f"simplebox-backend-run-{os.getpid()}-{self.__module_name}-{self.__func_name}-{ObjectsUtils.generate_random_str(6)}"
        self.__fifo_file = Path(gettempdir()).joinpath(f"simplebox-backend-fifo-{os.getpid()}-{self.__module_name}-{self.__func_name}-{ObjectsUtils.generate_random_str(6)}").absolute()

        self.__python_statement = StringBuilder(sep=" ", start='"', end='"')

        def import_module(modules: Iterable):
            for module in modules:
                if inspect.ismodule(module):
                    self.__python_statement.append("import").append(module.__name__ + ";")
                elif inspect.isfunction(module):
                    self.__python_statement.append("from").append(module.__module__) \
                        .append("import").append(module.__name__ + ";")
                elif inspect.isclass(module.__class__):
                    att_name = type(module).__name__
                    if att_name not in _inner_type:
                        if module.__module__ == "__main__":
                            self.__python_statement.append("from").append(self.__module_name) \
                                .append("import").append(module.__class__.__name__ + ";")
                        else:
                            self.__python_statement.append("from").append(module.__module__) \
                                .append("import").append(module.__class__.__name__ + ";")

        import_module(self.__all_args[0])
        import_module(self.__all_args[1].values())

        self.__python_statement.append("from") \
            .append(self.__module_name) \
            .append("import") \
            .append(self.__func_name + ";") \
            .append(f"from") \
            .append(_Runner.__module__) \
            .append("import") \
            .append(_run_module_name) \
            .append(";") \
            .append(f"{_run_module_name}(r'{str(self.__fifo_file)}', {self.__func_name})") \
            .append(" #").append(self.__flag)

    def __enter__(self):
        self.__fifo = open(self.__fifo_file, "w+b")
        pickle.dump(self.__all_args, self.__fifo, 0)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__fifo.close()

    def runner(self):
        os_name = os.name
        exec_func_name = f"_Backend__run_{os_name.lower()}_cmd"
        exec_func = getattr(self, exec_func_name, None)
        if exec_func:
            exec_func()
            self.__message_builder.append(";").append(f"process tag => {self.__flag}")
            _logger.log(level=20, msg=self.__message_builder.string(), stacklevel=3)
        else:
            raise RuntimeError(f"Unsupported operating systems: {os_name}")

    def __run_nt_cmd(self):
        """
        windows run
        """
        cmd = StringBuilder(sep=" ")
        cmd.append(executable) \
            .append("-c") \
            .append(self.__python_statement.string())
        if self.__log_path:
            cmd.append(">").append(self.__log_path).append("2>&1 &")
        self.__sub_process(cmd.string())
        self.__get_pid_nt()

    def __run_posix_cmd(self):
        """
        unix-like run
        """
        cmd = StringBuilder(sep=" ")
        cmd.append("nohup") \
            .append(executable) \
            .append("-c") \
            .append(self.__python_statement.string()) \
            .append(">")
        if self.__log_path:
            cmd.append(self.__log_path)
        else:
            cmd.append("/dev/null")
        cmd.append("2>&1 &")
        self.__sub_process(cmd.string())
        self.__get_pid_unix()

    def __get_pid_nt(self):
        cmd = StringBuilder(sep=" ")
        cmd.append("wmic") \
            .append("process") \
            .append("where") \
            .append("\"") \
            .append("commandline") \
            .append("like") \
            .append(f"'%%{self.__flag}%%'") \
            .append("and") \
            .append("name") \
            .append("!=") \
            .append("'WMIC.exe'") \
            .append("and") \
            .append("name") \
            .append("like") \
            .append("'python%'") \
            .append("\"") \
            .append("get") \
            .append("processid")
        process = Popen(cmd.string(), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                        encoding=getpreferredencoding(False))
        out, err = process.communicate()
        if process.returncode == 0 and "ProcessId" in out:
            message = StringUtils.trip(out.split('ProcessId')[1])
        else:
            message = f"error: {StringUtils.trip(err)}"
        self.__message_builder.append(f"Pid => {message}")

    def __get_pid_unix(self):
        cmd = StringBuilder(sep=" ")
        cmd.append("ps") \
            .append("-ef") \
            .append("|") \
            .append("grep") \
            .append("-v") \
            .append("grep") \
            .append("|") \
            .append("grep") \
            .append("-w") \
            .append(self.__flag) \
            .append("|") \
            .append("awk") \
            .append("'{print $2}'")
        process = Popen(cmd.string(), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                        encoding=getpreferredencoding(False))
        out, err = process.communicate()
        if StringUtils.is_not_empty(out):
            message = StringUtils.trip(out)
        else:
            message = f"error: {StringUtils.trip(err)}"
        self.__message_builder.append(f"Pid => {message}")

    def __sub_process(self, cmd: String):
        print(cmd)
        Popen(cmd, cwd=self.__run_path, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)


def backend_run(func: Callable, args: Iterable = None, kwargs: Dict = None, log_path: str or Path = None):
    """
    Create a new process and then run it in background mode
    Built-in data types are recommended for args and kwargs values type
    if use virtual environment,maybe resulting two process.it's python features.
    executing directly in the terminal also results in two processes.
    @params func: callback functions, real business code enter
    @params args: func's args
    @params kwargs: func's kwargs
    @params log_path: record the execution results of the backend,default not save log
    Use:
        class User(object):

            def __init__(self, name, age):
                self.name = name
                self.age = age


        class A(object):
            pass


        def run_args(user):
            with open("b_tmp2.txt", "w") as f:
                f.write("run_args ok!")


        def run_inner_args(user, args):
            for i in range(10):

                sleep(1)
            with open("b_tmp3.txt", "w") as f:
                f.write("run_inner_args ok!")


        def run():
            index = 0
            while True:
                if index == 10:
                    break
                sleep(1)
                index += 1
            with open("b_tmp1.txt", "w") as f:
                f.write("run ok!")


        def main():
            backend(run)
            parse = ArgumentParser()
            args = parse.parse_args()
            user = User("luo", 20)
            backend(run_args, args=(user, ))
            backend(run_inner_args, args=({'name': 'Teddy', 'age': 30}, args))


        if __name__ == '__main__':
            main()
    """
    with _Backend(func, args, kwargs, log_path) as bkd:
        bkd.runner()


__all__ = [backend_run]
