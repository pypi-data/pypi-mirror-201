import threading
import time
import sys
import traceback
from inspect import currentframe, getframeinfo
from agora_logging import logger
from .file_provider import FileProvider
from .command_line_provider import CommandLineProvider
from .environment_variable_provider import EnvironmentVariableProvider
from .file_key_provider import FileKeyProvider
from .dict_of_dict import DictOfDict
from .last_value_callbacks import LastValueCallbacks

class ConfigSingleton(DictOfDict):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def get_main_module_name(self):
        main_module_spec = sys.argv[0]
        if main_module_spec is None:
            return '__main__'
        else:
            return main_module_spec

    def __init__(self):
        super().__init__()
        self.callbacks = []
        self.setting_callbacks = {}

        config_defaults["Name"] = self.get_main_module_name()
        config_defaults["DEVICE_ID"] = "UNKNOWN"
        config_defaults["GROUP_ID"] = "UNKNOWN"
        config_defaults["GATEWAY_ID"] = "UNKNOWN"
        
        self.primary_config = FileProvider("AEA.json")
        self.evp = EnvironmentVariableProvider()
        self.clp = CommandLineProvider()        
        self.alt_config = FileProvider("config/AEA.json")
        self.fkp = FileKeyProvider()

        self.build()
        self.__start_monitoring()  # start monitoring the providers

    def observe(self,setting:str,callback):
        """
        Creates an observable setting and returns the current value
        """
        if setting not in self.setting_callbacks:
            if setting in super().get_dict():
                self.setting_callbacks[setting] = LastValueCallbacks(super().get_dict()[setting])
            else:
                self.setting_callbacks[setting] = LastValueCallbacks("")
        self.setting_callbacks[setting].append(callback)

    def stop_observing(self, setting: str, callback):
        if setting in self.setting_callbacks:
            self.setting_callbacks[setting].remove(callback)
    
    def observe_config(self,fn):
        self.callbacks.append(fn)

    def stop_observing_conf(self,fn):
        if fn in self.callbacks:
            self.callbacks.remove(fn)    
              
    def build(self):
        #print("rebuilding config")
        super().clear()
        #print (f"build this 0: {super().get_dict()}")
        #print (f"  add defaults: {config_defaults.get_dict()}")
        if isinstance(config_defaults, DictOfDict):
            super().merge(config_defaults.get_dict())
        #print (f"build this 1: {super().get_dict()}")
        #print (f"  add primary: {self.primary_config.get_dict()}")
        self.primary_config.check_for_updates()
        super().merge(self.primary_config.get_dict())        
        #print (f"build this 2: {super().get_dict()}")
        #print (f"  add environ: {self.evp.get_dict()}")
        super().merge(self.evp.get_dict())
        #print (f"build this 3: {super().get_dict()}")
        #print (f"  add commandline: {self.clp.get_dict()}")
        super().merge(self.clp.get_dict())
        #print (f"build this 4: {super().get_dict()}")
        #print (f"  add alt: {self.alt_config.get_dict()}")
        self.alt_config.check_for_updates()
        super().merge(self.alt_config.get_dict())
        #print (f"build this 5: {super().get_dict()}")
        #print (f"  add fkp: {self.fkp.get_dict()}")
        self.fkp.check_for_updates()
        super().merge(self.fkp.get_dict())
        #print (f"build this 6: {super().get_dict()}")
        #print (f"  add overrides: {config_overrides.get_dict()}")
        if isinstance(config_overrides, DictOfDict):
            super().merge(config_overrides.get_dict())
        #print (f"final       : {super().get_dict()}")
        self.__dispatch()


    def __dispatch(self):
        for callback in self.callbacks:
            callback()
        for key, value in self.setting_callbacks.items():
            #print(f"checking key {key}")
            #print(super().get_dict())
            if self.__getitem__(key) != "":
                #print(f"key in super_dict{key}")
                value.update(self.__getitem__(key))
            elif value.last_value != "":
                value.update("")


    def __listen_for_changes(self):
        while( self.should_run == True \
              and threading.main_thread().is_alive()):
            time.sleep(1)
            if ( self.primary_config.check_for_updates() or
                 self.alt_config.check_for_updates() or
                 self.fkp.check_for_updates()):
                self.build()
        

    def __start_monitoring(self):
        self.should_run = True
        t = threading.Thread(target=self.__listen_for_changes)
        t.start()


    def stop(self):
        self.should_run = False


def __set_logging_level(level):
    if level != "":
        logger.debug( f"logging_level changed to {level}")
        logger.set_level(level)



config_overrides = DictOfDict()
config_defaults = DictOfDict()

config = ConfigSingleton()
config.observe("AEA2:LogLevel",__set_logging_level)
__set_logging_level(config["AEA2:LogLevel"])


def log_except_hook(*exc_info):
    """
    Handles unhandled exceptions
    """
    exception=exc_info[1]
    tb_obj=exc_info[2]
    text="".join(traceback.format_tb(tb_obj))

    frameinfo= getframeinfo(currentframe())
    logger.write_unhandled_exception(exception,f'''Unhandled exception: {text}''',frameinfo)

    config.stop()

sys.excepthook = log_except_hook
