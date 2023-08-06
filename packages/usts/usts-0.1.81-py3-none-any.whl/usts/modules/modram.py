from ..utils import format_bytes
from ..module import Module

try: import psutil 
except: print("ModuleRAM: psutil module not found!")

class ModuleRAM(Module):

    def __init__(self,  str_format: str="RAM: {percent}{data_format}",
                        data_format: str="%", periodic: float=1.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format     = str_format
        self.data_format    = data_format

    def execute(self) -> str:
        vm = psutil.virtual_memory()

        data_types = [
            "total", "available", "percent", "used",
            "free", "active", "inactive", "buffers",
            "cached", "shared", "slab"
        ]

        result = self.str_format
        for data_type in data_types:
            raw_ram = vm.__getattribute__(data_type)
            ram     = str(format_bytes(raw_ram, self.data_format))
            result  = result.replace("{"+data_type+"}", ram) 

        result = result.replace("{data_format}", self.data_format)
        return result



