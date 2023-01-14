import unittest
from write_or_read_file import *


class Test(unittest.TestCase):

    def test_read_previous_days(self):
        # This checks that the method read_previous_days in write_or_read_file does not read current day.

        file = WriteOrReadFile("test_file_data")
        previous_days, day_list = file.read_previous_days()
        file_data = {'reading': {'2022-05-05': 20, '2022-05-02': 20, '2022-05-01': 20},
                     'writing': {'2022-05-05': 20, '2022-05-02': 20, '2022-05-01': 20}}
        self.assertEqual(previous_days, file_data, "The method should not read current day data.")

    def test_read_current_day(self):
        # This checks that the method read_current_day in in write_or_read_file does not read previous days.
        file = WriteOrReadFile("test_file_data")
        current_day = file.read_current_day()
        file_data = {'reading': 20, 'writing': 20}
        self.assertEqual(current_day, file_data, "The method should not read previous days' data.")

    def test_time_goal_percent(self):
        # This checks that the method time_goal_percent in in write_or_read_file works accordingly.
        file = WriteOrReadFile("test_file_data")
        time_goal_percents = file.time_goal_percents()
        time_goal_percent_reading = ((80 / (0.5 * 3600)) * 100).__round__()
        time_goal_percent_writing = ((80 / (5 * 3600)) * 100).__round__()
        file_data = {'reading': time_goal_percent_reading, 'writing': time_goal_percent_writing}
        self.assertEqual(time_goal_percents, file_data, "Time goal percent was wrong.")

    def test_activity_in_file(self):
        # This checks that the method time_goal_percent in in write_or_read_file works accordingly.
        file = WriteOrReadFile("test_file_data")
        text_list = file.read_file()
        activity_in_file, row = file.activity_in_file("running", text_list) # running is not included in the text_list
        self.assertFalse(activity_in_file, "The method should return False.")

if __name__ == "__main__":
    unittest.main()
