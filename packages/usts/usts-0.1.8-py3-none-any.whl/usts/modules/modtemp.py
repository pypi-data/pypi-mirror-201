from ..module import Module

try: import psutil 
except: print("ModuleTemp: psutil module not found!")

class ModuleTemp(Module):

    def __init__(self, str_format: str="CPU Temp: {k10temp}°", periodic: float=1.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format = str_format

    def execute(self) -> str:
        tempsd = psutil.sensors_temperatures()

        result = self.str_format
        for tempkey in tempsd.keys():
            tempstruct = tempsd[tempkey][0]
            cur_temp = tempstruct.__getattribute__("current")
            result = result.replace("{"+tempkey+"}", str(round(cur_temp, 1)))

        return result

