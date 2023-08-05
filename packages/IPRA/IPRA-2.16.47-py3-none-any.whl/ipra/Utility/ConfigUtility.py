import configparser
import os

class _ConfigSingleton:
    _configInstance = None
    _defaultINIPath = "C:\IPRA\config.ini"
    _defaultDirectory = "C:\IPRA"

    def __init__(self) -> None:
        self.config_obj = configparser.ConfigParser()
        configParam = self.config_obj.read(self._defaultINIPath)

        if len(configParam) == 0:
            #no config found,write default
            self.WriteDefault()
            pass

        pass


    def IsConfigExist(self,section,key):
        if not self.config_obj.has_section(section):
            return False
        else:
            if self.config_obj.has_option(section,key):
                return True
            else:
                return False
    
    def ReadConfig(self,section,key):
        #call IsConfigExist before
        return self.config_obj[section][key]
    
    def WriteConfig(self,section,key,value):
        if not self.config_obj.has_section(section):
            self.config_obj.add_section(section)

        self.config_obj.set(section=section,option=key,value=value)

        if not os.path.exists(self._defaultINIPath):
            os.makedirs(self._defaultDirectory,0o777)

        with open(self._defaultINIPath, 'w') as configfile:
            self.config_obj.write(configfile)
    
    def WriteDefault(self):
        self.WriteConfig('report_path','outputpath','C:/IPRA/REPORT')
        self.WriteConfig('report_path','inputpath','C:/IPRA/REPORT')
        self.WriteConfig('resource_path','resourcepath','C:/IPRA/RESOURCE/')
        self.WriteConfig('logger_path','loggerpath','C:/IPRA/LOG/')
        self.WriteConfig('default_download_report','default','False')
        self.WriteConfig('language','display','zh')
        self.WriteConfig('insurer','pru_agent_cd','0')
        self.WriteConfig('insurer','pru_user_id','0')



def GetConfigSingletion():
    if _ConfigSingleton._configInstance is None:
        _ConfigSingleton._configInstance = _ConfigSingleton()
    return _ConfigSingleton._configInstance