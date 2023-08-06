from ..module import Module

try: import psutil 
except: print("ModuleCpu: psutil module not found!")

class ModuleCPU(Module):

    def __init__(self, str_format: str="CPU: {data}%", periodic: float=1.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format = str_format

    def execute(self) -> str:
        return self.str_format.replace("{data}", str(psutil.cpu_percent()))

