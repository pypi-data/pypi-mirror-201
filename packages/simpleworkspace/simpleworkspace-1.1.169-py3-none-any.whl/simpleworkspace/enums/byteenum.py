from enum import Enum as _Enum
class ByteEnum(_Enum):
    B = 1
    KB = 1000
    MB = KB * 1000
    GB = MB * 1000
    TB = GB * 1000

    def GetStringRepresentation(self, byteCount: int, precisionDecimals=2):
        """
        :param prefix: b, kb, mb, gb
        """
        if self == ByteEnum.B:
            return str(byteCount) + " B"
        elif self == ByteEnum.KB:
            return str(round(byteCount / ByteEnum.KB.value, precisionDecimals)) + " KB"
        elif self == ByteEnum.MB:
            return str(round(byteCount / ByteEnum.MB.value, precisionDecimals)) + " MB"
        elif self == ByteEnum.GB:
            return str(round(byteCount / ByteEnum.GB.value, precisionDecimals)) + " GB"
        elif self == ByteEnum.TB:
            return str(round(byteCount / ByteEnum.TB.value, precisionDecimals)) + " TB"
        return
