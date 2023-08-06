from .cfg import Config
from .modules.modcpu import ModuleCPU
from .modules.modram import ModuleRAM
from .modules.modtime import ModuleTime

import datetime
import time
import os

class UStatus:

    def __init__(self, execute="stdout", update_periodic: float=1.0, separator: str=' | '):
        """
        :param execute [stdout / setxroot]  -> do actions with status:
            stdout      - just print it,
            setxroot    - setxroot -name "status"
        :param update_periodic              -> time when status is updated
        :param separator                    -> separator between items
        """
        self.is_exec            = True
        self.update_periodic    = update_periodic
        self.separator          = separator
        self.items              = self.make_items()

        self.config = Config()
        cfg = self.config.load_config()
        if hasattr(cfg, 'execute'): execute = cfg.execute
        if hasattr(cfg, 'items'):   self.items = cfg.items
        if hasattr(cfg, 'update_periodic'): 
            self.update_periodic = cfg.update_periodic
        if hasattr(cfg, 'separator'):
            self.separator = cfg.separator

        self.execute = self.make_execute(execute)

    def make_execute(self, execute_str):
        execs = {
            "stdout"    : self.stdout,
            "setxroot"  : self.xsetroot, 
        }
        if not execute_str in execs.keys():
            raise KeyError(f"{execute_str} not in execute list!")
        return execs[execute_str]

    def make_items(self) -> list:
        return [
            ModuleCPU(),
            ModuleRAM(),
            ModuleTime(), 
        ]

    def make_status_string(self) -> str:
        status = ""
        if self.items is None: return status

        for item in self.items:
            status += item.text + self.separator
        return status[:-len(self.separator)]

    def stdout(self):
        status = self.make_status_string()
        print(f"\r{(len(status)+10) * ' '}", end='\r')
        print(f"\r{status}", end='\r')

    def xsetroot(self):
        status = self.make_status_string()
        try: os.system(f'xsetroot -name "{status}"')
        except Exception as e: raise e

    def wait_for_zero_time(self):
        now = datetime.datetime.now()
        wait = 1000000 - now.microsecond
        time.sleep(wait/1000000)

    def exec(self):
        self.wait_for_zero_time()
        for item in self.items:
            item.exec()
        while self.is_exec:
            self.execute()
            time.sleep(self.update_periodic)
        for item in self.items:
            item.is_exec = False


