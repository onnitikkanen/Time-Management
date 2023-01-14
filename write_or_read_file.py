import datetime


class WriteOrReadFile:
    def __init__(self, filename):
        self.file = None
        self.filename = filename

    def write_into_file(self, current_activity, time_goal, written_text):
        # Writes into a text file.
        text_list = self.read_file()
        activity_in_file, row = self.activity_in_file(current_activity, text_list)
        if activity_in_file:
            self.file = open(self.filename, "w")
            activity_line = text_list[row - 1]
            activity_line_parts = activity_line.split(";")
            activity_line = activity_line_parts[0] + ";" + activity_line_parts[1] + ";" + written_text + "," + \
                            activity_line_parts[2]
            text_list[row - 1] = activity_line
            self.file.writelines(text_list)
            self.file.close()
        else:
            self.file = open(self.filename, "a")
            self.file.write(current_activity + ";" + str(time_goal) + ";" + written_text + "\n")
            self.file.close()

    def read_file(self):
        # Reads a text file.
        self.file = open(self.filename, "r")
        text_list = self.file.readlines()
        self.file.close()
        return text_list

    def activity_in_file(self, current_activity, text_list):
        # Checks if an activity is in the text file.
        row = 1
        for line in text_list:
            line = line.split(";")
            if line != "":
                activity = line[0]
                if activity == current_activity:
                    return True, row
                row += 1
        return False, 0

    def time_goal_percents(self):
        # Calculates the time goal percents of the activities in the text file.
        time_goal_percents = {}
        text_list = self.read_file()
        for line in text_list:
            cumulative_time_spent = 0
            line = line.split(";")
            if len(line) == 3:
                activity = line[0]
                time_goal = float(line[1]) * 3600
                time_data = line[2].rstrip("\n")
                time_data = time_data.split(",")
                for daily_data in time_data:
                    daily_data = daily_data.split("-")
                    time_spent = int(daily_data[3])
                    cumulative_time_spent += time_spent
                time_goal_percent = ((cumulative_time_spent / time_goal) * 100).__round__()
                time_goal_percents[activity] = min(time_goal_percent, 100)
        return time_goal_percents

    def read_current_day(self):
        # Creates a dictionary consisting of the activities and their cumulative times during the current day.
        current_day = {}
        time_goal_percents = {}
        text_list = self.read_file()
        for line in text_list:
            cumulative_time_spent = 0
            line = line.split(";")
            if len(line) == 3:
                activity = line[0]
                time_goal = float(line[1]) * 3600
                time_data = line[2].rstrip("\n")
                time_data = time_data.split(",")
                first_day = time_data[0].split("-")
                first_date = "-".join(first_day[0:3])
                for daily_data in time_data:
                    daily_data = daily_data.split("-")
                    date = "-".join(daily_data[0:3])
                    if date == first_date:
                        today = str(datetime.date.today())
                        if today == date:
                            time_spent = int(daily_data[3])
                            cumulative_time_spent += time_spent
                current_day[activity] = cumulative_time_spent
                time_goal_percent = ((cumulative_time_spent / time_goal) * 100).__round__()
                time_goal_percents[activity] = min(time_goal_percent, 100)
        return current_day

    def read_previous_days(self):
        # Creates a dictionary consisting of the activities and their time history before the current date.
        # Additionally, creates a list consisting of all of the dates.
        previous_days = {}
        text_list = self.read_file()
        today = str(datetime.date.today())
        day_list =[]
        for line in text_list:
            line = line.split(";")
            if len(line) == 3:
                activity = line[0]
                time_data = line[2].rstrip("\n")
                time_data = time_data.split(",")
                first_day = time_data[0].split("-")
                first_date = "-".join(first_day[0:3])
                daily_time_spent = 0
                previous_date = None
                buffer = 0
                current_day = {}
                for i in range(len(time_data)):
                    daily_data = time_data[i]
                    daily_data = daily_data.split("-")
                    date = "-".join(daily_data[0:3])
                    if date != today:
                        day_list.append(date)
                        time_spent = int(daily_data[3])
                        if previous_date is None:
                            previous_date = date
                        if date == previous_date:
                            daily_time_spent += time_spent
                            if buffer == len(time_data) - 1:
                                current_day[date] = daily_time_spent
                        else:
                            current_day[previous_date] = daily_time_spent
                            daily_time_spent = time_spent
                            if buffer == len(time_data) - 1:
                                current_day[date] = time_spent
                        previous_date = date

                    buffer += 1
                previous_days[activity] = current_day

        return previous_days, day_list

