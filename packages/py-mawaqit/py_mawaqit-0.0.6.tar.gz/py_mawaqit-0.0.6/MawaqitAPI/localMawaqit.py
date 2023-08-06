import json
from datetime import datetime
from MawaqitAPI.scraper import Crawler
from MawaqitAPI.helper import Helper

class LocalMawaqit():
    def __init__(self, fileName):
        """
        Class to interact with the loaded data, without having to scrape the website.
        Args:
            fileName (str): The name of the file that contains the data.

        
        """
        if fileName == None:
            #ignore this class
           
            return

        self.fileName = fileName
        self.helper = Helper()
        self.data = self.helper.load_data_from_file(self.fileName)
        self.day, self.month, self.year = self.helper.date_to_dd_mm_yyyy(self.helper.current_date())
        self.day = int(self.day)
        self.month = int(self.month)
        

    def get_prayer_times(self):
        """
        Returns:
            dict: A dictionary with the prayer times.
        """
        return self.helper.format_prayer_log(self.data["calendar"][self.month-1][str(self.day)])
    
    def get_prayer_time(self, prayer):
        """
        Args:
            prayer (str): The prayer you want to get the time of. Can be fajr, dhuhr, asr, maghrib or isha.

        Returns:
            str: The time of the prayer.
        """
        
        if prayer == "fajr":
            return self.data["calendar"][self.month-1][str(self.day)][0]
        elif prayer == "shurooq":
            return self.data["calendar"][self.month-1][str(self.day)][1]
        elif prayer == "dhuhr":
            return self.data["calendar"][self.month-1][str(self.day)][2]
        elif prayer == "asr":
            return self.data["calendar"][self.month-1][str(self.day)][3]
        elif prayer == "maghrib":
            return self.data["calendar"][self.month-1][str(self.day)][4]
        elif prayer == "isha":
            return self.data["calendar"][self.month-1][str(self.day)][5]
        else:
            return "Invalid prayer"

        
    def get_shurooq(self):
        """
        Returns:
            str: The time of shurooq.
        """
        return self.data["calendar"][self.month-1][str(self.day)][1]
        
        
    def get_jumua(self):
        """
        Returns:
            str: The time of jumua.
        """
        return self.data["calendar"][self.month-1][str(self.day)][2]
    
    def get_prayer_times_by_date(self, date_string):
        """
        Args:
            date_string (str): The date you want to get the prayer times of, format: dd-mm-yyyy.

        Returns:
            dict: The prayer times of the date.
        """
        day, month, year = self.helper.date_to_dd_mm_yyyy(date_string)
        day = int(day)
        month = int(month)
        return self.helper.format_prayer_log(self.data["calendar"][month-1][str(day)])
    
    def get_data(self):
        return self.data
        
    

