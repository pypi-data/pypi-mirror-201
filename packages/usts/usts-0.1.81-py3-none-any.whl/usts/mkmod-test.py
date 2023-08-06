import importlib
import inspect
import sys
import os

from module import Module 

class ModMan:

    def __init__(self) -> None:
        self.extension  = '.py'
        self.modules_path = os.path.dirname(os.path.abspath(__file__)) + "/modules"
        sys.path.append(self.modules_path)

    def inspect_obj(self, obj):
        return inspect.isclass(obj) and issubclass(obj, Module) and obj != Module 

    def add_module_from_file(self, mfile, filename) -> None:
        for it in dir(mfile):
            obj = getattr(mfile, it)
            if self.inspect_obj(obj):
                module = obj()
                self.__setattr__(filename.replace("-", "_"), module)

    def load_modules(self):
        for filename in os.listdir(self.modules_path):
            if filename.endswith(self.extension):
                filename = filename[:-3]

                path = f"modules.{filename}"
                pfile = importlib.import_module(name=path, package=f'modules.{filename}')
                self.add_module_from_file(pfile, filename)

if __name__ == "__main__":
    m = ModMan()
    m.load_modules()
    print(m.__dict__)

