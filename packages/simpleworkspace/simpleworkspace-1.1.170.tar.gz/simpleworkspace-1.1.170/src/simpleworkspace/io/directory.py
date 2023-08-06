from typing import Callable as _Callable
import os as _os

def Create(path: str):
    '''Create all non existing directiores in specified path'''
    _os.makedirs(path, exist_ok=True)

def List(
        searchDir: str,
        callback: _Callable[[str], None] = None,
        includeDirs=True, includeFiles=True,
        includeFilter:str|_Callable[[str],bool]=None,
        satisfiedCondition: _Callable[[str], bool] = None,
        exceptionCallback: _Callable[[Exception], None] = None,
        maxRecursionDepth: int=None
        ) -> (list[str] | None):
    """
    Recursively iterate all driectories in a path.
    All encountered exceptions are ignored

    @param callback
        feeds full filepath to a callback
    @param includeFilter
        * Callback or Regex string
            * callback that takes the fullpath and returns true for paths that should be included
            * regex string which searches full path of each file, if anyone matches a callback is called. Example: "/mySearchCriteria/i"
    @param satisfiedCondition
        takes a callback that returns a bool, if it returns true, no more search is performed
    @param exceptionCallback
        run callback on any raised exception
    @param maxRecursionDepth
        Specify how many levels down to list folders, level/depth 1 is basically searchDir entries
    @returns
        if no callback is given, a list of all found filepaths will be returned\n
        otherwise None
    """
    from queue import Queue
    import simpleworkspace.utility.regex

    if not _os.path.exists(searchDir):
        return

    # only returned if callback was not given
    allEntries = [] if (callback is None) else None

    currentFolderDepth = 1 #this is basically the base directory depth with its entries and therefore the minimum value
    folders = Queue()
    folders.put(searchDir)
    while folders.qsize() != 0:
        currentFolder = folders.get()
        try:
            currentFiles = _os.listdir(currentFolder)
            for filePath in currentFiles:
                filePath = _os.path.join(currentFolder, filePath)

                if(includeFilter is None):
                    pathMatchesIncludeFilter = True
                elif(isinstance(includeFilter, str)):
                    pathMatchesIncludeFilter = simpleworkspace.utility.regex.Match(includeFilter, filePath) is not None
                else: #callback
                    pathMatchesIncludeFilter = includeFilter(filePath)

                if _os.path.isfile(filePath):
                    if (includeFiles and pathMatchesIncludeFilter):
                        if callback is not None:
                            try:
                                callback(filePath)
                            except Exception as e:
                                if(exceptionCallback is not None):
                                    exceptionCallback(e)
                        else:
                            allEntries.append(filePath)
                else:
                    if (includeDirs and pathMatchesIncludeFilter):
                        if callback is not None:
                            try:
                                callback(filePath)
                            except Exception as e:
                                if(exceptionCallback is not None):
                                    exceptionCallback(e)
                        else:
                            allEntries.append(filePath)
                    folders.put(filePath)
                if satisfiedCondition is not None and satisfiedCondition(filePath):
                    return
            currentFolderDepth += 1
            if (maxRecursionDepth is not None) and (currentFolderDepth > maxRecursionDepth):
                break
        except Exception as e:
            if(exceptionCallback is not None):
                exceptionCallback(e)
    return allEntries


def Remove(path: str) -> None:
    '''removes a whole directory tree'''
    import shutil
    shutil.rmtree(path, ignore_errors=True)
