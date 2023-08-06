import time

class Timer:
    def __init__(self):
        self._start_time=None
        self.paused=True
        self.__running_total=0
    @property
    def curtime(self):
        if self._start_time is None:
            raise RuntimeError
        if self.paused:
            return self.__running_total
        return self.__running_total+(time.perf_counter()-self._start_time)
    def pause(self):
        if not self.paused:
            self.__running_total=self.curtime
            self.paused=True
    def start(self):
        if self.paused:
            self._start_time=time.perf_counter()
            self.paused=False
            
