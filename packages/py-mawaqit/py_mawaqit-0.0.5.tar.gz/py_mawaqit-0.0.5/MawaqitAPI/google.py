import pychromecast
from MawaqitAPI.constants import ADHAN_URL

class ChromeCast():
    """
    A class to control a Google Chromecast device. To play the adhan
    Args:
        friendly_name (str): The name of the device you want to control.

    """
    def __init__(self, friendly_name):
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[friendly_name])
        print(chromecasts)
        self.cast = chromecasts[0]
        self.cast.wait()
        self.mc = self.cast.media_controller
    
        """
        Args:
        volume (float): The volume to set the device to. Must be between 0 and 1.
        """
    def set_volume(self, volume):
        self.cast.set_volume(volume)
    
    """
    Args:
        url (str): The url of the media you want to play.
        media_type (str): The type of the media you want to play. example: "audio/mp3"
    """
    def play(self, url, media_type):
        self.mc.play_media(url, media_type)
        self.mc.block_until_active()
    
        """
        Pauses the media playing on the device.
        """
    def pause(self):
        self.mc.pause()
    
        """
        gets the status of the device.
        """
    def get_status(self):
        return self.mc.status

if __name__ == "__main__":
    cast = ChromeCast("Living Room speaker")
    cast.set_volume(0.4)
    cast.play(ADHAN_URL, "audio/mp3")
    print(cast.get_status())
    
    

#Living Room speaker