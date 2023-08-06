import requests_html, json
from MawaqitAPI.helper import Helper
class Crawler():
    """
    Crawler class that gets the data from the website.

    Args:
        mosque_id (str): The id of the mosque you want to get the data from. Can be found in the url of the mosque.
    """
    def __init__(self, mosque_id) -> None:

        self.url = "https://www.mawaqit.net/en/" + mosque_id
        self.elements = {
            "fajr": "/html/body/div[9]/div/div[3]/div[1]/div[2]/div",
            "dhuhr": "/html/body/div[9]/div/div[3]/div[2]/div[2]/div",
            "asr": "/html/body/div[9]/div/div[3]/div[3]/div[2]/div",
            "maghrib": "/html/body/div[9]/div/div[3]/div[4]/div[2]/div",
            "isha": "/html/body/div[9]/div/div[3]/div[5]/div[2]/div",
            "shurooq": "/html/body/div[9]/div/div[2]/div[7]/div[1]/div[2]/div[2]/div",
            "jumua": "/html/body/div[9]/div/div[2]/div[7]/div[3]/div/div[2]/div/div",
            "script_data": "/html/body/script[1]/text()"
        }
        self.mosque_id = mosque_id
        self.session = requests_html.HTMLSession()
        self.website_data = self.session.get(self.url)
        self.website_data.html.render()
        self.helper = Helper()

    # get prayer times from html elements
    def get_prayer_times(self) -> dict:
        fajr = self.website_data.html.xpath(self.elements["fajr"])[0].text
        dhuhr = self.website_data.html.xpath(self.elements["dhuhr"])[0].text
        asr = self.website_data.html.xpath(self.elements["asr"])[0].text
        maghrib = self.website_data.html.xpath(self.elements["maghrib"])[0].text
        isha = self.website_data.html.xpath(self.elements["isha"])[0].text
        return {
            "fajr": fajr,
            "dhuhr": dhuhr,
            "asr": asr,
            "maghrib": maghrib,
            "isha": isha
        }
    
    def get_prayer_time(self, prayer) -> str:
        if prayer in self.elements:
            return self.website_data.html.xpath(self.elements[prayer])[0].text

    def get_shurooq(self) -> str:
        return self.website_data.html.xpath(self.elements["shurooq"])[0].text

    def get_jumua(self) -> str:
        return self.website_data.html.xpath(self.elements["jumua"])[0].text

    def get_data(self) -> json:
        """
        Get the data from the website.

        Returns:
            json: The data from the website.

        """
        start_string = "var confData = "
        end_string = "]}]};"
    
        script_data = self.website_data.html.xpath(self.elements["script_data"])[0]
        start_index = script_data.find(start_string)
        end_index = script_data.find(end_string)
        data = script_data[start_index:end_index+4]
        data = data.replace(start_string, "")

        return json.loads(data)
    

    def get_prayer_times_by_date(self, date) -> dict:
        """
        Get the prayer times for a specific date.

        Args:
            date (str): The date you want to get the prayer times for. Format: DD-MM-YYYY

        Returns:
            dict: A dictionary with the prayer times.
        
        """

        day, month, year = date.split("-")
        day = int(day)
        month = int(month)

        #get data
        data = self.get_data()
        #get prayer times
        prayers = data["calendar"][month-1][str(day)]
        #remove second element
        

        return self.helper.format_prayer_log(prayers)





    







    

    


