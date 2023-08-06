# ChromeCast Adhan
This python script will allow you to use your chromecast as your personal adhan at home. Download the MawaqitAPI library and run this script.
At the bottom of the script you can initialize the mosque id, adhan url and the volumes of each prayer. You can run this on a server or a Raspberry Pi.
```python
from MawaqitAPI.mawaqit import Mawaqit
from MawaqitAPI.google import ChromeCast
from MawaqitAPI.constants import ADHAN_URL
from dateutil import parser
import time, threading

def main(mosque_id, cast_name, fajr_vol, duhur_vol, asr_vol, maghrib_vol, isha_vol, adhan):
    #set the chromecast name
    cast = ChromeCast(cast_name)

    last_update = 0
    prayertimes = {}
    #initialize the mawaqit object

    mawaqitAPI = Mawaqit(mosque_id, new_data=True)
    next_prayer = ""
    data = mawaqitAPI.get_prayer_times()

    while True:
        
        #get new data at 03:00
        if time.strftime("%H:%M") == "03:00" or time.strftime("%H:%M") == "03:01" or time.strftime("%H:%M") == "02:59" and time.time() - last_update > 60*60:
            data = mawaqitAPI.get_prayer_times()
            print(data)
            last_update = time.time()


        #convert prayer times to seconds

        prayertimes["fajr"] = parser.parse(data["fajr"]).timestamp()
        prayertimes["dhuhr"] = parser.parse(data["dhuhr"]).timestamp()
        prayertimes["asr"] = parser.parse(data["asr"]).timestamp()
        prayertimes["maghrib"] = parser.parse(data["maghrib"]).timestamp()
        prayertimes["isha"] = parser.parse(data["isha"]).timestamp()

        #get the next prayer
        for prayer in prayertimes:
            if time.time() < prayertimes[prayer]:
                next_prayer = prayer
                break

        print(next_prayer)
        print(prayertimes[next_prayer])
        
        #open other thread to print time left
        def print_time_left():
            while True:
                print("Time left for: " + next_prayer +  ": "+ time.strftime("%H:%M:%S", time.gmtime(prayertimes[next_prayer] - time.time())))
                time.sleep(1)

        t = threading.Thread(target=print_time_left)
        t.start()


        print("Time left for: " + next_prayer +  ": "+ time.strftime("%H:%M:%S", time.gmtime(prayertimes[next_prayer] - time.time())))
        #sleep until next prayer time
        time.sleep(prayertimes[next_prayer] - time.time())
        #play adhan
        #per prayer volume
        if next_prayer == "fajr":
            cast.set_volume(int(fajr_vol))
        elif next_prayer == "dhuhr":
            cast.set_volume(int(duhur_vol))
        elif next_prayer == "asr":
            cast.set_volume(int(asr_vol))
        elif next_prayer == "maghrib":
            cast.set_volume(int(maghrib_vol))
        elif next_prayer == "isha":
            cast.set_volume(int(isha_vol))
        
        cast.play(adhan, "audio/mp3")
        time.sleep(5)

if __name__ == "__main__":
    mosque_id = "essalam-rotterdam"
    cast_name = "Living Room speaker"
    fajr_vol = 0.4
    duhur_vol = 0.4
    asr_vol = 0.4
    maghrib_vol = 0.4
    isha_vol = 0.4
    adhan = ADHAN_URL
    main(mosque_id, cast_name, fajr_vol, duhur_vol, asr_vol, maghrib_vol, isha_vol, adhan)
```