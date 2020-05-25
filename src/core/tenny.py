"""
Core operations of Tenny the timer

Demo
    import tenny
    tenny.start_timer()
    'timer started at xx:xx:xx:xx (see tenny.now() to display current time)
    tenny.stop_timer()
    'timer stops at xx:xx::xxx'
    tenny.reset_timer()
    'timer reset at xx:xx:xxx'
"""


class Stopwatch:

    def __init__(self):

        self.time = None
        self.timer = None

    def start_timer(self):

        ...

    def stop_timer(self):

        ...

    def reset_timer(self):

        ...
