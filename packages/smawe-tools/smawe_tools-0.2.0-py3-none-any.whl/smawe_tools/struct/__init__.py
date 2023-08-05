from types import ModuleType
import logging
import sys


class LoggingModule(ModuleType):

    def __getattr__(self, name):
        if "__getattr__" in sys.modules[__name__].__dict__:
            r = sys.modules[__name__].__dict__["__getattr__"](name)
            if not r:
                raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
            return r

    def __getattribute__(self, name):
        return super(LoggingModule, self).__getattribute__(name)

    def __setattr__(self, attr, value):
        if attr == "ENABLED_LOG":
            if value:
                logging.basicConfig(format="%(asctime)s:%(filename)s:%(threadName)s:%(levelname)s:%(message)s",
                                    level=logging.INFO)
        super().__setattr__(attr, value)


def __getattr__(name: str):
    if name.lower() == "debug":
        return True
