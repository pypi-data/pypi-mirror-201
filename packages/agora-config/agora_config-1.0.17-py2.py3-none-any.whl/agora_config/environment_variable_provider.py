import os
from .dict_of_dict import DictOfDict

class EnvironmentVariableProvider(DictOfDict):
    def __init__(self):
        super().__init__()
        self.my_dict = DictOfDict()
        for key,val in dict(os.environ).items():
            self._process(key, val)


    def _process(self, key: str, val: str):
        if key.startswith("AEA__"):
            super().__setitem__(key[5:], val)