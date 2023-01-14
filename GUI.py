import datetime
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLCDNumber, QPushButton, QLabel, QLineEdit, QGroupBox, QTabWidget,
                             QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QCheckBox, QButtonGroup)
from write_or_read_file import WriteOrReadFile
from activity import Activity

class GUI(QWidget):
    #This GUI is based on The Pomodoro Timer introduced by the author in [1].
    #References:
    """[1] Willman, Joshua. Modern PyQt : Create GUI Applications for Project Management, Computer Vision, and Data
    Analysis. 1st ed. 2021., Apress, 2021, https://doi.org/10.1007/978-1-4842-6603-8."""
    def __init__(self):
        super().__init__()
        self.current_run_activities = {}
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 500)
        self.setWindowTitle("Time Management")
        self.tab = QTabWidget(self)
        self.timer_tab = QWidget()
        self.timer_tab.setObjectName("Timer")
        self.this_day_tab = QWidget()
        self.this_day_tab.setObjectName("This Day")
        self.previous_days_tab = QWidget()
        self.previous_days_tab.setObjectName("Previous Days")
        self.tab.addTab(self.timer_tab, "Timer")
        self.tab.addTab(self.this_day_tab, "This Day")
        self.tab.addTab(self.previous_days_tab, "Previous Days")
        self.tab.setMinimumSize(80, 20)
        self.initWriterReader()
        self.initActivities()
        self.CurrentDayData()
        self.TimerTab()
        self.ThisDayTab()
        self.PreviousDaysTab()
        self.timer_on = False
        self.current_activity = None
        self.timer_activity = None
        self.show()

    def initWriterReader(self):
        # Initializes the file_data object.
        self.filename = "activity_times"
        self.file_data = WriteOrReadFile(self.filename)

    def TimerTab(self):
        # Initializes the timer tab.
        self.activity_lineedit = QLineEdit()
        self.activity_lineedit.setClearButtonEnabled(True)
        self.activity_lineedit.setPlaceholderText("Add a New Activity")
        self.timegoal_lineedit = QLineEdit()
        self.timegoal_lineedit.setClearButtonEnabled(True)
        self.timegoal_lineedit.setPlaceholderText("Add a Time Goal (Hours)")
        self.enter_button = QPushButton("Enter")
        self.enter_button.clicked.connect(self.EnterActivity)
        self.Clearcheckbox = QPushButton("Clear activity selection")
        self.Clearcheckbox.setGeometry(50, 50, 100, 120)
        self.Clearcheckbox.clicked.connect(self.ClearCheckbox)
        self.closebutton = QPushButton("Exit Program", self)
        self.closebutton.clicked.connect(self.ActivateClose)
        self.activity_h_box = QHBoxLayout()
        self.activity_h_box.addWidget(self.activity_lineedit)
        self.activity_h_box.addWidget(self.timegoal_lineedit)
        self.activity_h_box.addWidget(self.enter_button)
        self.activity_h_box.addWidget(self.closebutton)
        self.activities_v_box = QVBoxLayout()
        self.activity_v_box = QVBoxLayout()
        self.activity_v_box.addWidget(self.Clearcheckbox)
        self.activity_v_box.addLayout(self.activity_h_box)
        self.activity_v_box.addLayout(self.activities_v_box)

        self.activitycheckboxes = {}
        self.checkboxes = QButtonGroup()
        for activity_obj in self.activity_objects:
            self.checkbox = QCheckBox(activity_obj.name, self)
            self.checkbox.clicked.connect(self.CurrentActivity)
            self.checkboxes.addButton(self.checkbox)
            self.activitycheckboxes[activity_obj] = self.checkbox
            self.activity_v_box.addWidget(self.checkbox)
        activities_gb = QGroupBox("Activities")
        activities_gb.setLayout(self.activity_v_box)
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(self.tab)
        main_v_box.addWidget(activities_gb)
        self.setLayout(main_v_box)
        self.startbutton = QPushButton("Start")
        self.startbutton.clicked.connect(self.StartTimer)
        self.stopbutton = QPushButton("Stop")
        self.stopbutton.clicked.connect(self.StopTimer)
        self.stoptime = QLabel()
        button_h_box = QHBoxLayout()
        button_h_box.addWidget(self.startbutton)
        button_h_box.addWidget(self.stopbutton)
        v_box = QVBoxLayout()
        v_box.addLayout(button_h_box)
        v_box.addWidget(self.stoptime)
        self.timer_tab.setLayout(button_h_box)
        self.timer_tab.setLayout(v_box)

    def CurrentDayData(self):
        #Calls the WriteOrReadFile class for the method read_current_day.
        self.current_day = self.file_data.read_current_day()
        self.time_goal_percents = self.file_data.time_goal_percents()


    def ThisDayTab(self):
        # Initializes the This day Tab. Creates a table that shows the activities and their time history during
        # the current date. Additionally,prints the time goal percent that has been achieved so far.
        self.text = QLabel()
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(len(self.current_day.keys()))
        index = 0
        for activity in self.current_day.keys():
            timespan = self.current_day.get(activity)
            hours, minutes, seconds = self.ConvertTime(timespan)
            time_string = "{:02d}:{:02d}:{:02d} ({:.03g}%)".format(hours, minutes, seconds,
                                                                   self.time_goal_percents.get(activity))
            self.tableWidget.setItem(0, index, QTableWidgetItem(activity))
            self.tableWidget.setItem(1, index, QTableWidgetItem(time_string))
            index += 1
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.this_day_tab.setLayout(layout)

    def PreviousDaysTab(self):
        # Initializes the Previous Days Tab. Creates a table that shows the activities and their time history before
        # the current date.
        previous_days, day_list = self.file_data.read_previous_days()
        find_max = 0
        for key in previous_days.keys():
            if len(previous_days.get(key)) > find_max:
                find_max = len(previous_days.get(key))
        max_date = max(day_list).split("-")
        min_date = min(day_list).split("-")
        date1 = datetime.date(int(min_date[0]), int(min_date[1]), int(min_date[2]))
        date2 = datetime.date(int(max_date[0]), int(max_date[1]), int(max_date[2]))
        days = (date2-date1).days + 1
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(days+1)
        self.tableWidget.setColumnCount(len(previous_days.keys())+1)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Date"))

        activity_index = 1
        for item in previous_days.keys():
            self.tableWidget.setItem(0, activity_index, QTableWidgetItem(item))
            date_index = 1
            for i in range(1, days + 1):
                date = datetime.date.today() - datetime.timedelta(days=i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(date)))
                for date_data in previous_days.get(item):
                    timespan = previous_days.get(item)[date_data]
                    hours, minutes, seconds = self.ConvertTime(timespan)
                    time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
                    if date_data == str(date):
                        self.tableWidget.setItem(date_index, activity_index, QTableWidgetItem(time_string))
                date_index += 1
            activity_index += 1
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.previous_days_tab.setLayout(layout)

    def initActivities(self):
        # Initializes the activities in the text file 'activity_times' and adds them to a list consisting of
        # the activities.
        activity_data = self.file_data.read_file()
        self.activity_objects = []
        for line in activity_data:
            line = line.split(";")
            if len(line) == 3:
                cumulative_time_spent = 0
                activity = line[0]
                time_goal = line[1]
                if time_goal is not None:
                    time_goal = float(time_goal)
                time_data = line[2].rstrip("\n")
                time_data = time_data.split(",")
                for daily_data in time_data:
                    daily_data = daily_data.split("-")
                    time_spent = float(daily_data[3])
                    cumulative_time_spent += time_spent
                activity_obj = Activity(activity, time_goal, cumulative_time_spent)
                self.activity_objects.append(activity_obj)

    def CurrentActivity(self):
        # updates the current activity if the checkbox of the corresponding activity is checked.
        for activity_obj in self.activitycheckboxes:
            if self.activitycheckboxes[activity_obj].isChecked():
                self.current_activity = activity_obj

    def ClearCheckbox(self):
        # Clears the checkboxes so that none of the checkboxes is checked.
        for activity_obj in self.activity_objects:
            self.checkboxes.removeButton(self.activitycheckboxes[activity_obj])
            self.activity_v_box.removeWidget(self.activitycheckboxes[activity_obj])
        for activity_obj in self.activity_objects:
            self.checkbox = QCheckBox(activity_obj.name, self)
            self.checkbox.clicked.connect(self.CurrentActivity)
            self.checkboxes.addButton(self.checkbox)
            self.activitycheckboxes[activity_obj] = self.checkbox
            self.activity_v_box.addWidget(self.checkbox)
        self.current_activity = None

    def StartTimer(self):
        # Starts the timer of the current activity. CHANGED! The StopTimer method is called here again as I figured
        # out how to stop the program from crashing.
        if self.timer_on:
            self.StopTimer()
        if self.current_activity is not None:
            self.current_activity.start_time()
            self.timer_activity = self.current_activity
            self.timer_on = True
        else:
            self.StartMessage()

    def StopTimer(self):
        # Stops the timer of the current activity. CHANGED: Prints the time spent on the activity today.
        if self.timer_on:
            self.timer_activity.stop_time()
            name, time_goal, time_string = self.timer_activity.upload_time()
            self.file_data.write_into_file(name, time_goal, time_string)
            seconds = int(time_string.split("-")[3])
            if name in self.current_day:
                self.current_day[name] += seconds
            else:
                self.current_day[name] = seconds
            self.timer_on = False
            hours, minutes, seconds = self.ConvertTime(self.current_day[name])
            self.runtime = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
            self.stoptime.setText("Your Have Spent {} Doing Activity '{}' Today.".format(self.runtime, name))

    def EnterActivity(self):
        # Checks that the user input is flawless. If the user input for the time goal is an integer, the method calls
        # for AddActivity, which creates an activity object of the activity.
        # If the time goal is not an integer, the method calls for ErrorMessage, which creates a message box alerting
        # of an error.
        activity_name = self.activity_lineedit.text()
        self.activity_lineedit.clear()
        time_goal = self.timegoal_lineedit.text()
        self.timegoal_lineedit.clear()
        if activity_name != "":
            if time_goal.strip().isdigit():
                self.AddActivity(activity_name, time_goal)
            else:
                self.ErrorMessage()
        else:
            self.ActivityNameMessage()

    def AddActivity(self, activity_name, time_goal):
        # Creates a new activity object if the activity does not already exist.
        for activity_obj in self.activity_objects:
            if activity_obj.name == activity_name:
                self.activity = activity_obj
        else:
            self.activity = Activity(activity_name, time_goal, 0)
            self.activity_objects.append(self.activity)
            self.checkbox = QCheckBox(self.activity.name, self)
            self.checkbox.clicked.connect(self.CurrentActivity)
            self.checkboxes.addButton(self.checkbox)
            self.activitycheckboxes[self.activity] = self.checkbox
            self.activity_v_box.addWidget(self.checkbox)

    def ErrorMessage(self):
        # Sends an error message if the user does not provide a time goal as an integer.
        error_msg = QMessageBox()
        error_msg.setWindowTitle("Error!")
        error_msg.setText("Time Goal Must Be an Integer!")
        error_msg.show()
        error_msg.exec_()

    def ActivityNameMessage(self):
        name_msg = QMessageBox()
        name_msg.setWindowTitle("Error!")
        name_msg.setText("Activity Must Have a Name!")
        name_msg.show()
        name_msg.exec_()

    def StartMessage(self):
        # Prevents the program from crashing if the user does not choose an activity before starting the timer.
        start_msg = QMessageBox()
        start_msg.setWindowTitle("Error!")
        start_msg.setText("Choose an Activity Before Starting the Timer!")
        start_msg.show()
        start_msg.exec_()

    def ConvertTime(self, seconds):
        # Converts time from seconds to hours, minutes and seconds.
        hours = (seconds / 3600) % 3600
        minutes = (seconds / 60) % 60
        seconds = seconds % 60
        return int(hours), int(minutes), int(seconds)

    def ActivateClose(self):
        # Closes the GUI and stops the timer when the closebutton is clicked.
        self.StopTimer()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(style_sheet)
    window = GUI()
    sys.exit(app.exec_())
