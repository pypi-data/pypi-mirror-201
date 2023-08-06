from ..module import Module

try: import psutil 
except: print("ModuleBattery: psutil module not found!")

class ModuleBattery(Module):

    def __init__(self, str_format: str="{percent}{icon}({secsleft}min)", periodic: float=5.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format = str_format

    def get_charge_icon(self, is_plugged: bool) -> str:
        if is_plugged:  return "⚡"
        else:           return "%"

    def execute(self) -> str:
        battery = psutil.sensors_battery()
        if battery is None: return "Battery not found!" 

        icon        = self.get_charge_icon(battery.power_plugged)
        percent     = str(battery.percent)
        secsleft    = str(round(battery.secsleft/60, 1))

        result = self.str_format.replace("{percent}", str(percent))
        result = result.replace("{icon}", icon)
        result = result.replace("{secsleft}", secsleft)
        return result


