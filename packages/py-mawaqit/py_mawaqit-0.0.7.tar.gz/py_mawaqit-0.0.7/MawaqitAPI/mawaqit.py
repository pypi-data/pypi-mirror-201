from MawaqitAPI.scraper import Crawler
from MawaqitAPI.helper import Helper
from MawaqitAPI.localMawaqit import LocalMawaqit

class Mawaqit():
    def __init__(self, mosque_id, new_data=True, **kwargs):

        """
        Args:
            mosque_id (str): The mosque id of the mosque you want to get the data from. example: "mosque_id" in https://www.mawaqit.net/en/mosque_id
            new_data (bool): *OPTIONAL* If set to True, the data will be scraped from the website. If set to False, the data will be loaded from the file (default data.json).
            file_name (str): *OPTIONAL* The name of the file to save the data in. Defaults to data.json.
        """
        self.mosque_id = mosque_id
        self.crawler = Crawler(mosque_id)
        self.new_data = new_data
        self.file_name = kwargs.get("file_name", "data.json")
        if self.new_data:
            self.local_mawaqit = LocalMawaqit(None)
        else:
            self.local_mawaqit = LocalMawaqit(self.file_name)

        self.helper = Helper()
       
    # create prayers list so user can use it to get prayer times
    def get_prayer_times(self):
        """
        Returns:
            dict: A dictionary with the prayer times. Fajr, Dhuhr, Asr, Maghrib, Isha
        """
        if self.new_data:
            return self.crawler.get_prayer_times()
        else:
            return self.local_mawaqit.get_prayer_times()

    def get_prayer_time(self, prayer):

        """
        Args:
            prayer (str): The prayer you want to get the time of. Can be fajr, dhuhr, asr, maghrib or isha.

        Returns:
            str: The time of the prayer.
        """
        
        if self.new_data:
            return self.crawler.get_prayer_time(prayer)
        else:
            return self.local_mawaqit.get_prayer_time(prayer)
    
    def get_shurooq(self):

        """
        Returns:
            str: The time of shurooq.
        """

        if self.new_data:
            return self.crawler.get_shurooq()
        else:
            return self.local_mawaqit.get_shurooq()

    def get_jumua(self):

        """
        Returns:
            str: The time of jumua.
        """

        if self.new_data:
            return self.crawler.get_jumua()
        else:
            return self.local_mawaqit.get_jumua()
    
    def get_data(self):

        """
        Returns:
            json: The data of the mosque in json format, all available data from the mawaqit website.
        """

        if self.new_data:
            return self.crawler.get_data()
        else:
            return self.local_mawaqit.get_data()
    
    def to_timestamp(self, date_string):

        """
        Args:
            date_string (str): The date you want to convert to a timestamp.

        Returns:
            int: The timestamp of the date.
        """

        return self.helper.get_timestamp(date_string)
    
    def get_prayer_times_by_date(self, date_string):

        """
        Args:
            date_string (str): The date you want to get the prayer times of, format: dd-mm-yyyy.

        Returns:
            dict: The prayer times of the date. Fajr, Shurooq, Dhuhr, Asr, Maghrib, Isha.
        """

        if self.new_data:
            return self.crawler.get_prayer_times_by_date(date_string)
        else:
            return self.local_mawaqit.get_prayer_times_by_date(date_string)

    def time_left(self, prayer):

        """
        Args:
            prayer (str): The prayer you want to get the time left of. Can be fajr, dhuhr, asr, maghrib or isha. In the same day.

        Returns:
            int: The time left until the prayer in seconds.
        """

        if self.new_data:
            data = self.crawler.get_prayer_times()
            return self.helper.time_left(data[prayer])
        else:
            data = self.local_mawaqit.get_prayer_times()
            return self.helper.time_left(data[prayer])
    
    def save_data_to_file(self, data):

        """
        Args:
            data (str): The data you want to save to a file.
        """

        self.helper.save_data_to_file(data, self.file_name)

    def get_next_prayer(self):

        """
        Returns:
            str: The next prayer.
        """

        if self.new_data:
            return self.helper.get_next_prayer(self.crawler.get_prayer_times())
        else:
            return self.helper.get_next_prayer(self.local_mawaqit.get_prayer_times())

    


        

    