import network
import utime
import machine
import neopixel
import time
import gc
import sys


import cdjh_mqtt
import display
import wifimgr

# ssid = "staatsveiligheid42"
# passwd = 'blijfvanmijnerf!!'
thingName = "cdjhvlamt-71373"


def main():
    d = display.Display()
    mgr = wifimgr.ConnectionManager(d)
    c = mgr.get_connection()
    ssid = mgr.get_active_ssid()
    passwd = mgr.get_active_password()
    mgr = None
    c = None
    del wifimgr
    del sys.modules["wifimgr"]
    gc.collect()
    if (c):
        client = cdjh_mqtt.CDJHVlamtMQTTClient(thingName, ssid, passwd)
        client.run()
    else:
        d.text("Oei, we geraken niet op de wifi!!")
    


main()