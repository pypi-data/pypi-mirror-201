from ..utils import format_bytes
from ..module import Module

try: import os 
except: print("ModuleDisk: os module not found!")

class ModuleDisk(Module):

    def __init__(self,  str_format: str="{path}: {free}/{max}{data_format}", 
                        path: str="/", data_format: str="Gb", periodic: float=10.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format     = str_format
        self.data_format    = data_format
        self.path           = path

    def execute(self) -> str:
        statvfs = os.statvfs(self.path)
        
        data_types = {
            "max"       : statvfs.f_blocks,
            "free"      : statvfs.f_bfree,
            "available" : statvfs.f_bavail
        }
        
        result = self.str_format
        result = result.replace("{path}", self.path)
        for data_type in data_types.keys():
            data = statvfs.f_frsize * data_types[data_type]
            result = result.replace("{"+data_type+"}", 
                str(format_bytes(data, self.data_format)))
        result = result.replace("{data_format}", self.data_format)

        return result


