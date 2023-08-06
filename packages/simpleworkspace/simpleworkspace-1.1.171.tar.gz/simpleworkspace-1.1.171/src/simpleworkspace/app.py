from logging import Logger as _Logger
from simpleworkspace.settingsproviders import SettingsManager_JSON as _SettingsManager_JSON

class App:
    appName = None
    appCompany = None
    appTitle = None #example: "appname - appcompany"
    appHash = 0 #appname + appcompany hashed together, numeric hash
    path_currentAppData = ""            #windows example: 'C:\\Users\\username\\AppData\\Roaming\\AppCompany\\AppName'
    path_currentAppData_storage = None  #windows example: 'C:\\Users\\username\\AppData\\Roaming\\AppCompany\\AppName\\Storage'

    _loggerFilepath = None
    logger = None #type: _Logger
    settingsManager = None #type: _SettingsManager_JSON

    @classmethod
    def Setup(cls, appName, appCompany=None, extraIdentifier=None):
        '''
        @param extraIdentifier: used for creating a more unique apphash to identify this program, will be bundled with appName and appCompany
        '''
        import os
        import simpleworkspace.io.directory
        import simpleworkspace.io.path
        from simpleworkspace.logproviders import RotatingFileLogger

        cls.appName = appName
        cls.appCompany = appCompany
        cls.appTitle = appName
        if appCompany is not None:
            cls.appTitle += " - " + appCompany
        
        cls.appHash = hash((appName, appCompany, extraIdentifier))

        cls.path_currentAppData = simpleworkspace.io.path.GetAppdataPath(appName, appCompany)
        cls.path_currentAppData_storage = os.path.join(cls.path_currentAppData, "storage")
        simpleworkspace.io.directory.Create(cls.path_currentAppData_storage)
        
        cls._loggerFilepath = os.path.join(cls.path_currentAppData, "info.log")
        cls.logger = RotatingFileLogger.GetLogger( cls._loggerFilepath)

        cls.settingsManager = _SettingsManager_JSON(os.path.join(cls.path_currentAppData, "config.json"))
        cls.settingsManager.LoadSettings()
        return