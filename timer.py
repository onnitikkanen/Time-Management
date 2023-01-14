import datetime
import time


class Timer:
    def __init__(self, activity):
        self.activity = activity
        self.start_time = 0
        self.end_time = 0
        self.timespan = 0
        self.start_date = 0
        self.end_date = 0

    def start_timer(self):
        self.start_time = time.time()
        self.start_date = datetime.date.today()

    def stop_timer(self):
        self.end_time = time.time()
        self.timespan = self.end_time - self.start_time
        return self.timespan, self.start_date