from ..module import Module

try: import datetime
except: print("ModuleTime: datetime module not found!")

class ModuleTime(Module):

    def __init__(self, timestrf: str="%H:%M:%S %m.%d.%Y", periodic: float=1.0) -> None:
        super().__init__(periodic=periodic)
        self.timestrf = timestrf

    def execute(self) -> str:
        return datetime.datetime.now().strftime(self.timestrf)




