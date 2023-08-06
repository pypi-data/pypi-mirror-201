from ..module import Module

class ModuleStr(Module):

    def __init__(self, value: str, periodic: float=-1) -> None:
        super().__init__(periodic=periodic)
        self.value = value

    def execute(self) -> str:
        return self.value



