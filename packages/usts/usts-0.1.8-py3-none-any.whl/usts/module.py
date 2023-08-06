import threading
import time

class Module:

    def __init__(self, periodic: float=1.0) -> None:
        self.text       = ""
        self.periodic   = periodic
        self.is_exec    = True

        self.thread = threading.Thread(target=self.update)

    def execute(self) -> str:
        return ""

    def update(self) -> None:
        while self.is_exec:
            self.text = self.execute()
            if self.periodic == -1: return
            time.sleep(self.periodic)
        return

    def exec(self) -> None:
        self.thread.start()


