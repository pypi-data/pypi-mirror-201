from ..module import Module

try: from subprocess import check_output
except: print("ModuleXKBState: subprocess module not found!")

class ModuleXKBState(Module):
    """
    Display keyboard layout (lang) by using xkblayout-state tool
    Source: https://github.com/nonpop/xkblayout-state

    Used command: 
        xkblayout-state print %s
    """

    def __init__(self, str_format: str="{layout}", periodic: float=1.0) -> None:
        super().__init__(periodic=periodic)
        self.str_format = str_format

    def execute(self) -> str:
        return check_output(["xkblayout-state", "print", "%s"]).decode('utf-8')



