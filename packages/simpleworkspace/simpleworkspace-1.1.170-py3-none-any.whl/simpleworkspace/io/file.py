import hashlib as _hashlib
import os as _os
import string
from typing import Callable as _Callable

class FileInfo:
    """
    * all backslashes are replaced with forward ones for simplicity 
    * If no match can be found for any property, they will default to empty string
      
    """
    from functools import cached_property as _cached_property

    rawPath = ""
    '''the input path, example case: a/b/test.exe -> a/b/test.exe'''

    def __init__(self, filepath:str) -> None:
        self.rawPath = filepath.replace("\\", "/")

    @_cached_property
    def _HeadTail(self) -> tuple[str,str]:
        return _os.path.split(self.rawPath)
    
    @_cached_property
    def _FilenameSplit(self) -> str:
        return self.Head.rsplit(".", 1)

    @_cached_property
    def RealPath(self) -> str:
        '''converts the input path to an absolute path, example case: a/b/test.exe -> c:/a/b/test.exe'''
        return _os.path.realpath(self.rawPath).replace("\\", "/")

    @_cached_property
    def Tail(self) -> str:
        '''Retrieves everything before filename, example case: a/b/test.exe -> a/b/'''

        tail, head = self._HeadTail
        if(tail != ""): #if there is a path always append to end of directory a slash
            tail += "/"
        return tail

    @_cached_property
    def Head(self) -> str:
        '''Retrieves everything after last slash which would be the filename or directory, example case: a/b/test.exe -> test.exe'''

        tail,head = self._HeadTail
        return head
    
    @_cached_property
    def Filename(self) -> str:
        '''retrieves filename without extension, example case: a/b/test.exe -> test'''

        return self._FilenameSplit[0]
    
    @_cached_property
    def FileExtension(self) -> str:
        '''retrieves fileextension with dot, example case: a/b/test.exe -> .exe'''

        if(len(self._FilenameSplit) == 2):
            return "." + self._FilenameSplit[1]
        return ""


def Hash(filePath: str, hashFunc=_hashlib.sha256()) -> str:
    from simpleworkspace.types.byte import ByteEnum
    Read(filePath, lambda x: hashFunc.update(x), readSize=ByteEnum.MegaByte.value * 1, getBytes=True)
    return hashFunc.hexdigest()

def Read(filePath: str, callback: _Callable[[str | bytes], None] = None, readSize=-1, readLimit=-1, getBytes=False, normalizeLineEndings=True) -> (str | bytes | None):
    """
    :callback:
        the callback is triggered each time a file is read with the readSize, \n
        callback recieves one parameter as bytes or str depending on getBytes param
    :readSize: amount of bytes to read at each callback, default of -1 reads all at once\n
    :ReadLimit: Max amount of bytes to read, default -1 reads until end of file\n
    :getBytes: specifies if the data returned is in string or bytes format\n
    :NormalizeLineEndings: default True, if getBytes is false aka reading as string, then change \\r\\n to \\n \n

    :Returns
        if no callback is used, the filecontent will be returned\n
        otherwise None
    """
    from io import BytesIO, StringIO

    content = BytesIO()
    if not getBytes:
        content = StringIO()

    if (readSize == -1 and readLimit >= 0) or (readLimit < readSize and readLimit >= 0):
        readSize = readLimit

    openMode = "rb"
    totalRead = 0
    with open(filePath, openMode) as fp:
        while True:
            if readLimit != -1 and totalRead >= readLimit:
                break
            data = fp.read(readSize)
            totalRead += readSize
            if data:
                if not getBytes:
                    data = data.decode('utf-8', 'replace')
                    if normalizeLineEndings:
                        data = data.replace("\r\n", "\n")
                if callback is None:
                    content.write(data)
                else:
                    callback(data)
            else:
                break

    if callback is None:
        return content.getvalue()
    return None


    
def Create(filepath: str, data: bytes | str = None):
    if type(data) is str:
        data = data.encode()
    with open(filepath, "wb") as file:
        if data is not None:
            file.write(data)

def Append(filepath: str, data: bytes | str):
    if type(data) is bytes:
        pass  # all good
    elif type(data) is str:
        data = data.encode()
    else:
        raise Exception("Only bytes or string can be used to append to file")
    with open(filepath, "ab") as file:
        file.write(data)


def CleanInvalidNameChars(filename:str, allowedCharset = string.ascii_letters + string.digits + " .-_"):
    return ''.join(c for c in filename if c in allowedCharset)

def IsPossiblyBinary(filepath):
    textchars = bytearray([7,8,9,10,12,13,27]) + bytearray(range(0x20, 0x7f)) + bytearray(range(0x80, 0x100))
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars))

    text = Read(filepath, readLimit=1024, getBytes=True)
    return is_binary_string(text)