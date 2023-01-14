from timer import Timer


class Activity:
    def __init__(self, name, time_goal, time_spent):
        self.name = name
        self.time_goal = float(time_goal)
        self.time_spent = time_spent
        self.timer = Timer(self.name)
        self.timespan = 0
        self.current_time = 0
        self.date = 0

    def start_time(self):
        # Calls for the timer class to start the timer.
        self.timer.start_timer()

    def stop_time(self):
        # Calls for the timer class to stop the timer.
        self.timespan, self.date = self.timer.stop_timer()

    def time_string(self):
        # Creates a time string consisting of the date and timespan of the activity.
        start_date = str(self.date)
        timespan = str(self.timespan.__round__())
        return start_date + "-" + timespan

    def upload_time(self):
        return self.name, self.time_goal, self.time_string()
