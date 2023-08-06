from dateutil import parser
from datetime import datetime
import json

class Helper():

    def __init__(self):
        """
        Helper class that contains helper functions. Useful , repetitive functions that are used in multiple places.
        """
        pass

    def get_date_from_string(self, date_string):
        """
        Get the date from a string.

        Args:
            date_string (str): The date string.
        
        Returns:
            str: The date in the format DD-MM-YYYY.

        """
        return int(parser.parse(date_string).timestamp())

    def save_data_to_file(self, data, file_name):

        
        with open(file_name, "w") as f:
            #dump dict to file
            json.dump(data, f)

    def load_data_from_file(self, file_name):
        with open(file_name, "r") as f:
            #load dict from file
            return json.load(f)
        
    def date_to_dd_mm_yyyy(self, date_string):
        #return [day, month, year]
        day , month, year = date_string.split("-")
        return [day, month, year]
    
    def current_date(self):
        return datetime.now().strftime("%d-%m-%Y")
    
    def format_prayer_log(self, prayers):
        return {"fajr": prayers[0], "shurooq": prayers[1], "dhuhr": prayers[2], "asr": prayers[3], "maghrib": prayers[4], "isha": prayers[5]}
    
    def get_current_timestamp(self):
        return int(datetime.now().timestamp())
    
    def get_timestamp(self, date_string):
        return int(parser.parse(date_string).timestamp())
    
    def time_left(self, date_string):
        return self.get_timestamp(date_string) - self.get_current_timestamp()
    
    def get_next_prayer(self, prayers):
        for prayer in prayers:
            if self.time_left(prayers[prayer]) > 0:
                return prayer
    