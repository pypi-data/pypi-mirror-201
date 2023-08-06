import os as __os
import signal as __sig
import functools as __fn
import fileinput as __file
from detacher import detach as __detach

__all__ = {"daemon", "set_logfile", "remove_logfile", "end_daemon"}

__JETSAM_LOG = "/tmp/jetsam.log"


def daemon(func) -> None:
    """
    Decorator to detach function from Python interpreter
    Spawns a new python interpreter to run function within
    """

    @__fn.wraps(func)
    def wrap():
        __detach(func, func.__name__, __JETSAM_LOG)

    return wrap


def set_logfile(logfile: str) -> None:
    globals()["__JETSAM_LOG"] = logfile


def remove_logfile() -> None:
    __os.remove(globals()["__JETSAM_LOG"])


def end_daemon(func) -> None:
    global __JETSAM_LOG
    with __file.input(__JETSAM_LOG, inplace=True) as f:
        for line in f:
            (func_name, pid, state) = line.strip("\n").split(":")
            if func_name == func.__name__ and "running" == state:
                __os.kill(int(pid), __sig.SIGKILL)
                print(f"{func_name}:{pid}:dead")
            else:
                print(line, end="")
