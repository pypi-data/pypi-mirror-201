import json

class DictOfDict():
    '''
    This class was supposed to encapsulate the dict of dict within all providers... 
    '''
    def __init__(self):
        self.data = dict()

    def __getitem__(self, setting_name:str):
        keys = setting_name.split(':')
        # print(keys)
        ld = self.data
        for key in keys[:-1]:
            if isinstance(ld, dict) and key in ld:
                ld = ld[key]
            else:
                return ""
        if keys[-1] in ld:
            d = ld[keys[-1]]
            if not isinstance(d, dict):
                return d
            elif isinstance(d, dict):
                if len(d.keys()) == 0:
                    return ""
                return json.dumps(ld[keys[-1]])
        return ""
    
    def __setitem__(self, setting_name:str, value:str):
        #print( f"setting '{setting_name}' = '{value}'")
        setting_name = setting_name.replace("__", ":")
        keys = setting_name.split(':')
        ld = self.data
        for key in keys[:-1]:
            if isinstance(ld, dict) and key in ld:
                if not isinstance(ld[key], dict):
                    ld[key] = dict()
                ld = ld[key]
            else:
                nd = dict()
                ld[key] = nd
                ld = nd
        if not isinstance(ld, dict):
            ld = dict()
        ld[keys[-1]] = value
        #print(self.data)


    def remove(self, setting_name: str):
        #print( f"removing '{setting_name}'")
        setting_name = setting_name.replace("__", ":")
        keys = setting_name.split(':')
        ld = self.data
        for key in keys[:-1]:
            if isinstance(ld, dict) and key in ld:
                if not isinstance(ld[key], dict):
                    return
                ld = ld[key]
            else:
                return
        if isinstance(ld, dict):
            k = keys[-1]
            if k in ld:
                #print( ld )
                ld.pop(k)
            return
        return
    
   
    def get_dict(self):
        return self.data
    

    def merge(self, dict2):
        self.data = self.__merge(self.data, dict2)

    def __merge(self, dict1, dict2):
        for key in dict2:
            if key in dict1 and isinstance(dict1[key], dict) \
                            and isinstance(dict2[key], dict):
                self.__merge(dict1[key], dict2[key])
            else:
                if( isinstance(dict2[key], dict)):
                    dict1[key] = dict()
                    self.__merge(dict1[key], dict2[key])
                else:
                    dict1[key] = dict2[key]
        return dict1

    def clear(self):
        self.data.clear()

