"""__init__.py: general methods used on libsan"""
import inspect
import re
import sys


def _print(string):
    # name of the module that called the function
    module_name = inspect.currentframe().f_back.f_globals["__name__"]
    string = re.sub("DEBUG:", "DEBUG:(" + module_name + ")", string)
    string = re.sub("FAIL:", "FAIL:(" + module_name + ")", string)
    string = re.sub("FATAL:", "FATAL:(" + module_name + ")", string)
    string = re.sub("WARN:", "WARN:(" + module_name + ")", string)
    print(string)
    sys.stdout.flush()
    if "FATAL:" in string:
        raise RuntimeError(string)
