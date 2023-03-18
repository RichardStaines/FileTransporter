from threading import Timer
from datetime import datetime as dt


class RepeatedTimer(object):
    def __init__(self, interval, start_time, end_time, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.start_time = start_time
        self.end_time = end_time
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False

    def nSecs(self, time):
        pt = dt.strptime(time, '%H:%M:%S')
        total_seconds = pt.second + pt.minute * 60 + pt.hour * 3600
        return total_seconds

    def _run(self):
        self.is_running = False
        self.start()

        now_nsecs = self.nSecs(dt.now().strftime('%H:%M:%S'))
        if self.nSecs(self.start_time) <= now_nsecs <= self.nSecs(self.end_time):
            self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

