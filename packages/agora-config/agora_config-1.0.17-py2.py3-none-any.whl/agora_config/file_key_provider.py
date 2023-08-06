import pathlib
from agora_logging import logger
from .dict_of_dict import DictOfDict


class FileKeyProvider(DictOfDict):
    def __init__(self):
        super().__init__()
        self.key_folder = pathlib.Path("config/keys")
        self.last_modified_time = 0
        self.__check_time()


    def check_for_updates(self) -> bool:
        return self.__check_time()
    
    # private methods
            
    def __read_config(self) -> dict:
        super().clear()
        if self.key_folder.exists() and self.key_folder.is_dir():
            for file_path in self.key_folder.iterdir():
                if file_path.is_file():
                    try:
                        with file_path.open() as f:
                            contents = f.read()
                            if len(contents) > 0 and contents[-1] == '\n':
                                contents = contents[:-1]
                        #print(f"contents of '{file_path.name}' is '{contents}'")
                        self.__set(file_path.name, contents)
                    except Exception as e:
                        logger.exception(e, f"Could not load config file '{file_path}' : {str(e)}")


    def __set(self, key, value):
        new_dict = dict()
        current_dict = new_dict
        parts = key.split("__")
        if len(parts) > 0:
            for element in parts[:-1]:
                current_dict[element] = {}
                current_dict = current_dict[element]
            current_dict[parts[-1]] = value
        super().merge(new_dict)
    
    
    def __check_time(self) -> bool:
        """
        Checks if the times of any of the key-files or the key folder itself (i.e. a file create or delete) has changed 
        """
        mtime = 0
        modified = False
        if self.key_folder.exists() and self.key_folder.is_dir():
            try:
                mtime = self.key_folder.stat().st_mtime
                if mtime > self.last_modified_time:
                    # print( "key_folder modified" )
                    self.last_modified_time = mtime
                    modified = True
            except Exception as e:
                logger.exception(e, "Could not get key folder time. 'config/keys'")

            for file_path in self.key_folder.iterdir():
                if file_path.is_file():
                    try:
                        mtime = file_path.stat().st_mtime
                        #if file_path.name == "DEF":
                            # print( f"DEF mtime = {mtime}")
                        if mtime > self.last_modified_time:
                            #print( f"file '{file_path.name}' modified" )
                            self.last_modified_time =  mtime
                            modified = True                            
                    except Exception as e:
                        logger.exception(e, f"Could not get config file time. (config_file = '{self.key_folder}')")

            if modified == True:
                self.__read_config()
                return True
        return False