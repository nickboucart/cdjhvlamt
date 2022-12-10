import network
import utime
import time
import gc
import sys

import machine

import cdjh_mqtt
import display
import wifimgr
import animaties


thingName = ""
with open("name.txt", "r") as f:
    thingName = f.readline()

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

def setupWifiAndMQTT(display, animations, dingNaam):
    mgr = wifimgr.ConnectionManager(display)
    c = mgr.get_connection()
    ssid = mgr.get_active_ssid()
    passwd = mgr.get_active_password()
    mgr = None
    gc.collect()
    if ssid:
        client = cdjh_mqtt.CDJHVlamtMQTTClient(dingNaam, ssid, passwd, animations)
        client.run()
        print('alles runt!!')
    else:
        d.text("Oei, we geraken niet op de wifi!!")



def main():
    d = display.Display()
    aniMgr = animaties.AnimatieMgr(33, 30)
    aniMgr.stop_annimation_and_run_new_one("fire")
    def handleButtonPress(pin):
        aniMgr.stop()
    button = machine.Pin(0, mode = machine.Pin.IN)
    button.irq(trigger=machine.Pin.IRQ_RISING, handler=handleButtonPress)
    setupWifiAndMQTT(d, aniMgr, thingName)
    while True:
        asyncio.sleep(5)

#     asyncio.create_task(setupWifiAndMQTT(d, aniMgr, thingName))
#     while 1:
#         await asyncio.sleep(5)

main()