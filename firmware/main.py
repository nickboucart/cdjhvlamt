import network
import utime
import time
import gc
import sys


import cdjh_mqtt
import display
import wifimgr
import animaties


thingName = ""
with open("name.txt", "r") as f:
    thingName = f.readline()


def main():
    d = display.Display()
    mgr = wifimgr.ConnectionManager(d)
    c = mgr.get_connection()
    ssid = mgr.get_active_ssid()
    passwd = mgr.get_active_password()
    mgr = None
    c = None
#     del wifimgr
#     del sys.modules["wifimgr"]
    gc.collect()
    aniMgr = animaties.AnimatieMgr(33, 30)
    aniMgr.stop_annimation_and_run_new_one("fire")
    if ssid:
        client = cdjh_mqtt.CDJHVlamtMQTTClient(thingName, ssid, passwd, aniMgr)
        client.run()
    else:
        d.text("Oei, we geraken niet op de wifi!!")
    


main()