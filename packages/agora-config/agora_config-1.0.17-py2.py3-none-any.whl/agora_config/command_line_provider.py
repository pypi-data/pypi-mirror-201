import sys
from .dict_of_dict import DictOfDict

class CommandLineProvider(DictOfDict):
    def __init__(self):
        super().__init__()
        for arg in sys.argv:
            self._processArg(arg)

    # private methods
            
    def _processArg(self, arg:str):
        if arg.startswith("-d") and len(arg) > 2:
            first_equals = arg.find("=")
            if first_equals != -1:
                key = arg[2:first_equals]
                val = arg[first_equals+1:]
                super().__setitem__(key, val)
