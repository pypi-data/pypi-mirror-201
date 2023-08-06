from pyinstrument import Profiler


class StartStopProfiler:
    def __init__(self, interval=0.001, async_mode="enabled"):
        self.profiler = Profiler(interval, async_mode)
        self.running = False

    def __call__(self):
        if not self.running:
            self.profiler.start()
            self.running = True
        else:
            self.profiler.stop()
            self.running = False
            self.profiler.open_in_browser()


t = StartStopProfiler()
