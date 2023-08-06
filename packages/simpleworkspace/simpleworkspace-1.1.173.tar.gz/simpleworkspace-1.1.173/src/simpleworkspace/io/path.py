import os as _os

def FindEmptySpot(filepath: str):
    from simpleworkspace.io.file import FileInfo

    fileContainer = FileInfo(filepath)
    TmpPath = filepath
    i = 1
    while _os.path.exists(TmpPath) == True:
        TmpPath = f"{fileContainer.Tail}{fileContainer.Filename}_{i}{fileContainer.FileExtension}"
        i += 1
    return TmpPath

def GetAppdataPath(appName=None, companyName=None):
    """
    Retrieves roaming Appdata folder.\n
    no arguments        -> %appdata%/\n
    appName only        -> %appdata%/appname\n
    appname and company -> %appdata%/appname/companyName\n
    """
    from simpleworkspace.extlibs import appdirs

    return appdirs.user_data_dir(appName, companyName, roaming=True)
