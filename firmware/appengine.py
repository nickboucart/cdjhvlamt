import machine
import esp32

rtc = machine.RTC()

wakepin = machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_UP,hold=True)
cyclepin = machine.Pin(35, machine.Pin.IN, machine.Pin.PULL_UP,hold=True)
cyclepin_ext = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_UP,hold=True)

cyclepin_back = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP,hold=True)


apin = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP,hold=True)
bpin = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP,hold=True)
cpin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP,hold=True)


selpin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP,hold=True)
esp32.gpio_deep_sleep_hold(True)

esp32.wake_on_ext0(pin = wakepin, level = esp32.WAKEUP_ALL_LOW)


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
    if machine.wake_reason()== machine.PIN_WAKE:
        print("Because of pin")
    else:
        #Go back to sleep
        machine.deepsleep(3600000)

from machine import Pin, SPI
import st7789

import sys
import os
import json
import gc


#Lets us store data in the RTC ram area to persist between reboots
rtc_ram = {}




try:
    x = rtc.memory()
    if x:
        rtc_ram.update(json.loads(x.decode()))
except Exception as e:
    sys.print_exception(e)
    print("RTC Ram is not valid JSON")
    

config = {'fgcolor':st7789.color565(200,220,90),'bgcolor':st7789.color565(12,20,10)}

try:
    if "conf.json" in os.listdir():
        with open('conf.json') as f:
            config.update(json.load(f))
except Exception as e:
    print(e)
    

fontname = 0
titlefont = ''

appTickRate = 1000

unlocked = False

max_cpu_freq = 240000000
min_cpu_freq = 80000000
#max_cpu_freq = 80000000

import romanc as font

def selfnt(fnt):
    global titlefont
    global fontname
    if fontname and fontname in sys.modules:
        del sys.modules[fontname]
    
    try:
        if fnt =='roman':
            import romanc as f2
        elif fnt =='gothic':
            import gothita as f2
        elif fnt =='script':
            import scriptc as f2
        else:
            import romanc as f2
    except Exception:
        import romanc as f2
    titlefont =f2
    fontname = fnt
        

selfnt(config.get('titlefont',''))

def saveConf():
    x = ''
    try:
        if "conf.json" in os.listdir():
            with open('conf.json') as f:
                x = f.read()
    except:
        print("bad old")
            
    
    x2 = json.dumps(config)
    
    if not x ==x2:
        with open('conf.json','w') as f:
            f.write(x2)




appStack = []
appNameStack = []

tft_was_on = 1
tft = st7789.ST7789(
        SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19), miso=Pin(17)),
        135,
        240,
        reset=Pin(23, Pin.OUT),
        cs=Pin(5, Pin.OUT),
        dc=Pin(16, Pin.OUT), 
        backlight=Pin(4, Pin.OUT),
        rotation=1)

cardOffset = 0

async def title(t):
    global tft_was_on
    global titlefont
    if tft_was_on:
        tft.fill_rect(0,0,tft.width(),39,config.get("titlebgcolor",0))
        tft.draw(titlefont,t,1,18,config.get("titlefgcolor",st7789.WHITE), 1)

async def card(icon,t,lines=[]):
    global tft_was_on
    global titlefont
    
    if icon == 'default':
        icon = config.get("default_icon",'')
        
    if tft_was_on:
        global cardOffset
        tft.fill(config.get("bgcolor",0))
        cardOffset = 0
        if icon:
            cardOffset = 100
            try:
                tft.jpg(icon,0,39)
            except Exception:
                pass
        await title(t)
        if lines:
            n=0
            for i in lines:
                await cardline(n,i)
                n+=1
        
async def cardline(n,t):
    global cardOffset
    global tft_was_on
    global font
    if tft_was_on:
        tft.fill_rect(cardOffset,(n*32)+39,tft.width()-cardOffset,32,config.get("bgcolor",0))
        tft.draw(font,t,cardOffset,(n*32)+49,config.get("fgcolor",st7789.WHITE),0.7)

evQ = [] 


import machine
import time



# Used for select button timestamp capture
ts = 0
tmpts = 0


endSleepOnSelPin = False

def captureTS(p):
    global ts
    global tmpts
    global endSleepOnSelPin
    global lastInteraction
    
    tmpts = time.ticks_ms()
    if p.value()==0:
        if tmpts > (ts+70):
            ts = tmpts

    lastInteraction= tmpts     
    
    if endSleepOnSelPin:
        time.cancel_sleep()

    
selpin.irq(trigger=Pin.IRQ_FALLING, handler=captureTS)



wifi_lock_ts = 0

#Let it be on initially, but able to be turned 
wifi_lock_mode = 0

# True if the wifi manager state thinks it was on           
wifi_was_on = False


def doWifi(setLocks=True):
    global wifi_lock_ts
    global wifi_lock_mode
    global wifi_was_on
    
    found = 0
    for i in appStack:
        if i.wifi_mode:
            found = max(found,i.wifi_mode)
    
    if found:
        if not wifi_was_on:
            w = nic.active()
            if not w:
                print("Set WiFi on")
                nic.active(True)
                nic.wifi_ps(network.WIFI_PS_MAX_MODEM)
            if not nic.isconnected():
                if (not nic.status()==network.STAT_CONNECTING) or not w:
                    try:
                        tryConnectWifi()
                    except Exception as e:
                        print(e)
                wifi_was_on=True
        if setLocks:
            wifi_lock_mode = found
    else:
        if wifi_lock_mode:       
            wifi_lock_ts = time.ticks_ms()
        if setLocks:
            wifi_lock_mode=0

def checkOldWifi(screenOn=True):
    global wifi_lock_ts
    global wifi_lock_mode
    global wifi_was_on

    if wifi_lock_mode:
        if screenOn or wifi_lock_mode >=2:
            wifi_lock_ts=time.ticks_ms()
            return
    
    if nic.active():
        # After 15s of no app needing it, turn it off.
        if time.ticks_diff(time.ticks_ms(), wifi_lock_ts) > 60000:
            print("Set WiFi off")
            wifi_was_on=False
            nic.active(False)


wakeLock = 0

def checkWakeLocks():
    global wakeLock
    wakeLock=0
    for i in appStack:
        if i.wake_mode>wakeLock:
            wakeLock = i.wake_mode
    
     
    

async def appExit(r, app):
    if(len(appStack)>1):
        a = appStack.pop()
        try:
            if appNameStack[-1]:
                del sys.modules[appNameStack[-1]]
        except:
            pass
        appNameStack.pop()
        #The app that called us
        c = app.caller
        
        await a.on_exit()
        if c== app.caller:
            if not c.dead:
                await c.on_return_value(r)
       
        checkWakeLocks()
        doWifi()
    while(not (selpin.value() and wakepin.value()) ):
        time.sleep(0.1)
    time.sleep(0.1)
                 






import gc

lastInteraction = 1
import gc
import os
import random

def rs(h):
    machine.reset()

async def USBCon():
    while(not (selpin.value() and wakepin.value())):
        time.sleep(0.1)
    time.sleep(1)
    await card(None,"USB Mode",['SEL to exit','flip cable if no work','Wait 5s before try connect'])

    selpin.irq(trigger=Pin.IRQ_FALLING, handler=rs)
    raise SystemExit



import os
import json
import network

nic = network.WLAN(network.STA_IF)
nic.wifi_ps(network.WIFI_PS_MAX_MODEM)

if 'hostname' in config:
    nic.config(dhcp_hostname=config['hostname'])
else:
    nic.config(dhcp_hostname="micropython")

def _connect(s,p):
    if p:
        nic.connect(s,p)
    else:
        nic.connect(s)
        
    nic.wifi_ps(network.WIFI_PS_MAX_MODEM)

def tryConnectWifi():
    if nic.ifconfig()[0]=='0.0.0.0':
        if not nic.active():
            print("Set Wifi on")
            nic.active(True)
            nic.wifi_ps(network.WIFI_PS_MAX_MODEM)

        if "wifi.json" in os.listdir():
            with open('wifi.json') as f:
                f = json.load(f)
                if f['ssid']:
                    try:
                        print("Try connect to:"+f['ssid'])
                        _connect(f['ssid'], f['psk'])
                    except Exception as e:
                        print(e)


        
#Connect a wifi and save it for future use
def connect_wifi(s,p):
    _connect(s,p)
    with open('wifi.json','w') as f:
        json.dump({'ssid': s, 'psk':p},f)




    
# Rules:
# There are 2 mandatory buttons, cycle and select
# Cycle is the one on the left or the top if there are two
# User programs cannot handle cycle long press, it is reserved for "exit"
# User programs may handle select long press.
# When there are more buttons, "right arrow" shall mean the same as select.
    
class LineMenuApp():
    # 0 none 1 while awake 2 always 3 highspeed
    wifi_mode = 0
    # 0 powerdown allowed
    # 1 screen off, cpu lightsleep
    # 2 screen on, cpu lightsleeep
    # 3 no sleep
    wake_mode = 0
    
    def __init__(self) -> None:
        self.selected = 0
        # All lines that we want to have in the menu
        self.lines = []

        # The top line shown on the screen
        self.topline = 0
        self.sleeping=False
        self.dead = False
        
    def keep_awake(self):
        global lastInteraction
        lastInteraction= time.ticks_ms()
                
    async def launch(self, app,*args,kiosk_lock=False):
        async def f():
            gc.collect()
            print("launch", app,gc.mem_free())
            global appTickRate
            if not isinstance(app,LineMenuApp):
                if app in apps:
    
                    a = apps[app]()
                    a.caller = self
                    appStack.append(a)
                    if kiosk_lock:
                        a.use_kiosk_lock = True
                    appNameStack.append("")
                    doWifi()
                    await a.on_app(*args)
                    appTickRate = await appStack[-1].on_tick() or 5000
                    checkWakeLocks()

                    return

            if isinstance(app,LineMenuApp):
                a= app
            else:
                a = __import__("app_"+app).App()
                
            if kiosk_lock:
                    a.use_kiosk_lock = True
            a.caller = self
            appStack.append(a)
            appNameStack.append(app)
            doWifi()
            await a.on_app(*args)
            gc.collect() 
            appTickRate = await appStack[-1].on_tick() or 5000 
            checkWakeLocks()
            
            
        evQ.append(f)
                
    async def draw_lines(self):
        global tft_was_on
        if self.selected>(self.topline+2) or self.selected<self.topline:
            self.topline = self.selected

        if tft_was_on:
            for i in range(min(3, len(self.lines))):
                l = (i+self.topline) % len(self.lines)
                p = ''
                if self.selected ==l:
                    p =">"
                t = self.lines[l]
                #Allow associating a value
                if isinstance(t, list):
                    t = t[0]
                if callable(t):
                    t = str(self.lines[l]())
                    
                await cardline(i,p+ t )
    
    async def on_cycle(self,ticks):
        self.keep_awake()
        self.selected+=ticks
        if self.lines:
            self.selected = self.selected % len(self.lines)
        else:
            self.selected =0
            
        if self.selected==0:
            self.topline=0
        elif self.selected> self.topline+2:
            self.topline= min(self.topline+3, len(self.lines)-1)

        await self.draw_lines()


    async def on_cycle_repeat(self,ticks):
        self.keep_awake()
        self.selected+=ticks
        self.selected = self.selected % len(self.lines)
        self.selected -= self.selected%3
        
        self.topline= self.selected
        await self.draw_lines()


    async def exit(self,r=None):
        print("exit",self)
        self.dead=True
        if not (hasattr(self, 'use_kiosk_lock') and self.use_kiosk_lock):
            await appExit(r,self)
        else:
            async def f():
                await appExit(r,self)
            await self.launch('core.lock',f)

    async def on_app(self,*args):
        pass
    
    async def on_return_value(self,arg):
        await self.redraw()
    
    async def on_exit(self):
        pass

    
    async def on_select(self, state,ts):
        pass
    
    async def on_sleep(self):
        self.sleeping = True
        
    async def on_wake(self):
        self.sleeping= False
        await self.redraw()
        
    async def on_tick(self):
        return 5000
    
    async def redraw(self):
        pass
    
    
class InfoApp(LineMenuApp):
    wifi_mode = 1
    def wlanStr(self):
        try:
            return nic.config('essid')[:12] +" "+ ('FAIL' if (nic.ifconfig()[0]=='0.0.0.0') else '')
        except:
            return "Wifi: 0%"
    
    def memStr(self):
        return "Mem: "+str(gc.mem_free())+"b"
    
    def tempStr(self):
        return "Tmp: "+str(esp32.raw_temperature())+"F"
    
    def magStr(self):
        return "Mag: "+str(esp32.hall_sensor())
       
    def tickStr(self):
        return "millis: "+str(time.ticks_ms())+"ms"
    
    async def on_app(self,a):
        await self.redraw()
    
    async def redraw(self):
        await card(None, "Status",[])
        self.lines = [self.wlanStr,self.memStr, self.magStr, self.tickStr,"Exit"]
        await self.draw_lines()

    async def on_select(self, state,ts):
        global lastInteraction
        if state==1:
            self.keep_awake()
            
            s = self.lines[self.selected]
            
            if s=="Exit":
                await self.exit()
                return
                        
        await self.draw_lines()








class TextApp(LineMenuApp):
    nums = " .+-/1234567890%()'?~_!@#$^&*`=[]{}\|"
    basefreq = " ETAONRISHDLFCMUGYPWBVKJXZQ"

    lsf={'t':" HETAORNISDLFCMUGYPWBVKJXZQ",
    'h': " EAIOTNRSHDLFCMUGYPWBVKJXZQ",
    'i': " NSTCEAIORHDLFMUGYPWBVKJXZQ",
    'e': " RNSDATCEIOHLFMUGYPWBVKJXZQ",
    'a': " NTRSCDBAEIOHLFMUGYPWVKJXZQ",
    'r': " EAOITNRSHDLFCMUGYPWBVKJXZQ",
    'o': " NRUFTSCEOAIHDLMGYPWBVKJXZQ"

    }
     
    async def on_app(self,arg):
        await card("default", "Text Edit",[])
        
        self.position = -1
        self.text = "" if arg is None else str(arg)
        
        self.initialtext = arg
         
        self.lines = ["Move","UPPER","lower","123!?.", "DEL", "Cancel", "Accept"]
        
        self.mode = "top"
        
        self.savedKBType = 2
        
        self.kb = self.basefreq
        self.lastchar = ''
        
        await self.draw_lines()
        await self.dispTitle()
        
    async def dispTitle(self):
        l = len(self.text) + 3
        o = ''
        
        if self.position==-1:
            o+='|'
                                                                                     
        for i in range(l):
            if i< len(self.text):
                o+=self.text[i]
            else:
                o+=" "
            
            if i==self.position:
                o+="|"

                
        p = max(0, self.position-12)
        await title(o[p:])
            
    async def on_select(self, state,ts):
        self.keep_awake()
        
        if self.mode == "top":
            if state==1:
                s = self.lines[self.selected]
                if s=='Move':
                    self.position+=1
                    if self.position >= len(self.text):
                        self.position = -1
                    await self.dispTitle()
                
                if s=="UPPER" or s=='lower' or s=='123!?.':
                    freq = self.basefreq

                    if self.lastchar.lower() in self.lsf:
                        freq=self.lsf[self.lastchar.lower()]
                        
                    if s =='UPPER':
                        self.kb = freq
                    elif s =='lower':
                        self.kb = freq.lower()
                    elif s =='123!?.':
                        self.kb = self.nums
                        
                    self.lines= self.kb     
                    self.text= self.text
                    self.savedKBType = self.selected
                    self.selected =0
                    self.topline =0
                    self.mode = "letters"
                    await self.draw_lines()
                    return
                
                if s=='DEL':
                    o=''
                    for i in range(len(self.text)):
                        o+=('' if self.position==i else self.text[i])
                    
                    self.position -= 1
                    if self.position<0:
                        self.position=-1
                    
                    self.text = o
                    await self.dispTitle()

                    
                # Cancel/accept
                if s=='Cancel':
                    await self.exit(self.initialtext)
                    return
                
                if s=='Accept':
                    await self.exit(self.text.strip())
                    return
                
        if self.mode == "letters":
            if state==1:
                
                oldPosition = self.position
                if self.position == -1:
                    self.position =0
                    
                o=''
                for i in range(len(self.text)):
                    o+=(self.text[i] + self.lines[self.selected] if self.position==i else self.text[i])
                     
                if self.position>= len(self.text):
                    o+=self.lines[self.selected]

                self.lastchar = self.lines[self.selected]
                
                if not oldPosition==-1:
                    self.position += 1
                self.selected = self.savedKBType
                self.topline = self.selected
                
                self.text = o
                self.mode="top"
                await self.dispTitle()
                self.lines = ["Move","UPPER","lower","123!?.", "DEL", "Cancel","Accept"]
                await self.draw_lines()
                


class NumPad(LineMenuApp):
    nums = "0123456789."
   
    async def on_app(self,val='',mode='int'):
        await card("default", "Num Edit",[])
        
        self.text = str(val)
        self.position = (len(self.text)-1) if len(self.text) else -1
        self.mode = mode
         
        self.lines = ["Cancel", "Accept","DEL"]+(['.'] if self.mode in ('str','float') else []) + list(self.nums)
        
        
        await self.draw_lines()
        await self.dispTitle()
        
    async def dispTitle(self):
        l = len(self.text) + 3
        o = ''
        
        if self.position==-1:
            o+='|'
            
        for i in range(l):
            if i< len(self.text):
                if self.mode =='password':
                    o+='*'
                else:
                    o+=self.text[i]
            else:
                o+=" "
            
            if i==self.position:
                o+="|"

                
        p = max(0, self.position-12)
        await title(o[p:])
            
    async def on_num_key(self,number, state):
        pass
    
    async def on_select(self, state,ts):
        self.keep_awake()
        if state==0:
            return
        
        s = self.lines[self.selected]
        print(s)
        
        if s=='DEL':
            o=''
            for i in range(len(self.text)):
                o+=('' if self.position==i else self.text[i])
            
            self.position -= 1
            if self.position<0:
                self.position=-1
            
            self.text = o

            
        # Cancel/accept
        elif s=='Cancel':
            await self.exit(None)
            return
        
        elif s=='Accept':
            await self.exit(self.text.strip())
            return
    
        else:
            
            oldPosition = self.position
            if self.position == -1:
                self.position =0
                
            o=''
            for i in range(len(self.text)):
                o+=(self.text[i] + self.lines[self.selected] if self.position==i else self.text[i])
                 
            if self.position>= len(self.text):
                o+=self.lines[self.selected]

            
            if not oldPosition==-1:
                self.position += 1
            self.selected = 0
            self.topline = 0

            
            self.text = o
        await self.dispTitle()
        await self.draw_lines()




# Immutable strings so they can be compiled in
fgs = """[
              ["green",48869],
              ["orange",64288],
              ["blue",25407],
              ["grey",31695],
              ["purple",36882],
              ["white",65535],
              ["yellow",65093],
              ["red",45056]
            ]
          
        """

bgs="""
[     ["black",0],
      ["paledarkgreen",2144],
      ["grey",6371],
      ["paledarkblue",2114],
      ["darkpurple",4097],
      ["green",6529],
      ["blue",2214],
      ["brown",14496],
      ["red",14368],
      ["yellow",14720]
      
      
    ]
"""


class ThemeApp(LineMenuApp):

    
    async def on_app(self,arg):
        await self.redraw()
        
        
    async def redraw(self):
        await card("default", "Theming",[])
        self.lines = ["Default Icon",
                      "Title Font","Title FG", "Title BG","FG Color", "BG Color","Exit"]
        await self.draw_lines()
        
    
    async def on_return_value(self,v):
        selfnt(config.get('titlefont',''))
        await self.redraw()
        
    async def on_select(self, state,ts):
        global lastInteraction
        if state==1:
            self.keep_awake()
            
            s = self.lines[self.selected]

            if s=="FG Color":
                await self.launch("core.configoption", 'fgcolor',json.loads(fgs))
                
            elif s=="BG Color":
                await self.launch("core.configoption", 'bgcolor',json.loads(bgs))

            elif s=="Title FG":
                await self.launch("core.configoption", 'titlefgcolor',json.loads(fgs))
                
            elif s=="Title BG":
                await self.launch("core.configoption", 'titlebgcolor',json.loads(bgs))
                
                
            elif s=="Title Font":
                await self.launch("core.configoption", 'titlefont',
                                                   [
                                                      ['Roman','roman'],
                                                      ['Script',"script"],
                                                      ['Gothic',"gothic"]
                                                    ]
                                                  )
                
            elif s=="Default Icon":
                x = [['No Icon','']]
                if "icons" in os.listdir("/"):
                    for i in os.listdir("/icons"):
                        x.append([i,"/icons/"+i])
                        
                await self.launch('core.configoption','default_icon',x)
                
            elif s=="Exit":
                await self.exit()
                return
                        
                
        await self.draw_lines()
    
    
    async def on_tick(self):
        return 5000


class SettingsApp(LineMenuApp):

    
    async def on_app(self,arg):
        await self.redraw()
        
    async def on_exit(self):
        saveConf() 
        
    async def redraw(self):
        await card("default", "Tools Menu",[])
        self.lines = ["USB","Sleep","Status","Passcode","Hostname","Boot App","Theme","Exit"]
        await self.draw_lines()
    
        
    async def on_select(self, state,ts):
        global lastInteraction
        if state==1:
            self.keep_awake()
            
            s = self.lines[self.selected]
            # USB connection is an "app"
            if s=="USB":
                await USBCon()
                
            if s=="Sleep":
                lastInteraction = -(3600*1000)
                
            if s=="Status":
                await self.launch("core.info",None)
                
            elif s=="Passcode":
                await self.launch("core.configoption", 'password',"int")
                
            elif s=="Hostname":
                await self.launch("core.configoption", 'hostname',"str")
          
            elif s=="Theme":
                await self.launch(ThemeApp(),None)
          
            elif s=="SleepTime":
                await self.launch("core.configoption", 'sleeptime',
                                                   [
                                                      ['Never',0],
                                                      ['10min',600],
                                                      ['1hr',3600],
                                                      ['3hr',3600*3]
                                                    ]
                                                  )
            elif s=="Boot App":
                x = [['App Launcher','']]
                
                for i in os.listdir("/"):
                    if i.startswith("app_") and i.endswith(".py"):
                        x.append([i[4:-3],i[4:-3]])
                await self.launch('core.configoption','default_app',x)


            elif s=="Exit":
                await self.exit()
                return
                        
                
        await self.draw_lines()
    
    
    async def on_tick(self):
        return 5000



class SettingOptionApp(LineMenuApp):
    
    async def on_app(self, *arg):
        
        # We don't test type... this would crash on 1 letter keys
        if arg[1] == "str":
            self.settingkey = arg[0]
            await self.launch("core.text",config.get(arg[0],''))
        elif arg[1] == "int":
            self.settingkey = arg[0]
            await self.launch("core.numpad",config.get(arg[0],''),'int')
        else:
            self.settingkey = arg[0]
            self.settingchoices = arg[1]
            await self.redraw()
        
    async def redraw(self):
        await card(None, self.settingkey)
        self.lines = self.settingchoices
        await self.draw_lines()
    
    async def on_select(self, state,ts):
        global lastInteraction
        if state==1:
            config[self.settingkey] = self.lines[self.selected][1]
            await self.exit(None)
            return
                
    async def on_return_value(self, val):
        config[self.settingkey] = val
        await self.exit(None)
            
    
    async def on_tick(self):
        return 5000






class LockedCallbackApp(LineMenuApp):
    
    async def on_app(self,arg):
        global unlocked
        self.callback = arg
        self.password = config.get('password','')
        if not self.password or unlocked:
            unlocked = True
            print('ul')
            await self.exit(True)
            await self.callback()
            return
                             
        await self.redraw()
                
                                                                                           
        
    async def redraw(self):
        print('rdc')
        await card("default", "Password",['Enter','Cancel'])
        self.lines = ["Enter","Cancel"]

        await self.draw_lines()             
    
    async def on_select(self, state,ts):
        print('osc')
        self.keep_awake()
        if state==1:
            if self.selected==0:
                await self.launch('core.numpad','','int')
            else:
                await self.exit('False')
            return
                 
        await self.draw_lines()
    
    async def on_return_value(self,v):
        global unlocked
        if v==self.password:
            unlocked = True
            await self.exit(True)
            await self.callback()
        else:
            
            await title("FAIL")
            time.sleep(5)
            await title("Password")
    
    
    async def on_tick(self):
        return 5000



class DialogApp(LineMenuApp):
    
    async def on_app(self,title, lines,cb):
        self.callback = cb
        self.title = arg
        self.lines = lines  
        await self.redraw()                                                                  
        
    async def redraw(self):
        await card("default", self.title, self.lines)
        await self.draw_lines()             
    
    async def on_select(self, state,ts):
        self.keep_awake()
        if state==1:
            self.callback(self.selected)
            await self.exit('False')
            return
                 
        await self.draw_lines()





class LauncherApp(LineMenuApp):
    
    async def on_app(self,arg):
        if config.get('default_app',''):
            try:
                print('ld')
                await self.launch(config.get('default_app',''),None,kiosk_lock=True)
                return
            except Exception as e:
                print(e)
            
        await self.redraw()
        
        
    async def redraw(self):
        await card("default", config.get('hostname','Apps'),[])
        self.lines = ["Settings"]
        
        for i in os.listdir("/"):
            if i.startswith("app_") and i.endswith(".py"):
                self.lines.append(i[4:-3])
                
        await self.draw_lines()             
    
    async def on_select(self, state,ts):
        self.keep_awake()
        if state==1:
            if self.selected==0:
                async def f():
                    await self.launch('core.settings',None)
                await self.launch('core.lock', f)
            else:
                await self.launch(self.lines[self.selected],None)
            return
                 
        await self.draw_lines()
    
    
    async def on_tick(self):
        return 5000
    
    

apps={
    'core.settings':SettingsApp,
    'core.configoption':SettingOptionApp,
    'core.info': InfoApp,
    'core.text': TextApp,
    'core.numpad': NumPad,
    'core.lock': LockedCallbackApp,
    'core.dialog':DialogApp

}


#########################
tft.init()
tft.fill(config.get("bgcolor",0))


numpinstates = bytearray(3)
numpinstates[0]=1
numpinstates[1]=1
numpinstates[2]=1

numpins = {1: apin, 2: bpin, 3: cpin}

def doNumPins():
    for i in numpins:
        v = numpins[i].value()
        if not v==numpinstates[i]:
            numpinstates[i] = v
            if v:
                await appStack[-1].on_num_key(i,1)
            else:
                await appStack[-1].on_num_key(i,0)
            

async def _run(app):
    global lastInteraction
    global endSleepOnSelPin
    global tft_was_on
    global appTickRate
    global unlocked
    
    lastCycleDown = 0
    lastSelCh = 0
    
    disablenextcycleup = 0
    
    cyclerepeat = 0
    
    appStack.append(app)
    
    #card("10.jpg","Test Title", ["Bat: 100%", "RAM: "+str(gc.mem_free()), "Temp: "+str(esp32.raw_temperature())+'F'])
    await appStack[-1].on_app(None)
    checkWakeLocks()
    doWifi()

    
    lastTick = 0

    # Dummy, cyclepin, selpin, cyclepin_back
    bstates = bytearray(4)
    bstates[1]=1
    bstates[2]=1
    bstates[3]=1

    try:
        while 1:
            if evQ:
                await evQ.pop()()
            
            # User interaction stuff happens at boosted frequency
            
            v = cyclepin.value() and cyclepin_ext.value()
            
            if not v == bstates[1]:
                bstates[1] = v
                cyclerepeat = time.ticks_ms()
                if disablenextcycleup:
                    disablenextcycleup = 0
                else:
                    # Pin change cycle pin 
                    if v==0:
                        lastCycleDown = time.ticks_ms()
                    else:
 
                         
                        if time.ticks_diff(time.ticks_ms(), lastCycleDown) < 1200:
                            print("CYC1")
                            await appStack[-1].on_cycle(1)
                            continue
            
            

             
            # Going to fake a bunch of press and releases if they hold it
            elif not v and time.ticks_diff(time.ticks_ms(),cyclerepeat)> 500:
                
                # When holding don't do normal up behavior
                disablenextcycleup = 1
                bstates[1] = v
                cyclerepeat = time.ticks_ms()
                
                # Pretend it was just down and now up
                lastCycleDown = cyclerepeat
                print("CYC3")
                await appStack[-1].on_cycle_repeat(3)

                continue
            
            
            
            v = cyclepin_back.value()
            
            if not v == bstates[3]:
                bstates[3] = v
                cyclerepeat = time.ticks_ms()
                if disablenextcycleup:
                    disablenextcycleup = 0
                else:
                    # Pin change cycle pin 
                    if v==0:
                        lastCycleDown = time.ticks_ms()
                    else:
 
                         
                        if time.ticks_diff(time.ticks_ms(), lastCycleDown) < 1200:
                            print("CYC-1")
                            await appStack[-1].on_cycle(-1)
                            continue
            
            

             
            # Going to fake a bunch of press and releases if they hold it
            elif not v and time.ticks_diff(time.ticks_ms(),cyclerepeat)> 500:
                
                # When holding don't do normal up behavior
                disablenextcycleup = 1
                bstates[3] = v
                cyclerepeat = time.ticks_ms()
                
                # Pretend it was just down and now up
                lastCycleDown = cyclerepeat
                print("CYC-3")
                await appStack[-1].on_cycle_repeat(-3)

                continue
            
            
            if time.ticks_diff(time.ticks_ms(), lastSelCh)>70:
                lastSelCh=time.ticks_ms()
                v = selpin.value() and wakepin.value()
                if not v == bstates[2]:
                    print("SEL")
                    # Pin change select pin
                    await appStack[-1].on_select(v,ts)
                     
                    bstates[2] = v
                    continue

            if wakeLock < 2 and ((time.ticks_diff(time.ticks_ms(),lastInteraction) > 20000) or lastInteraction==0):
                tft.off()
                tft.sleep_mode(1)
                tft_was_on=False
                print("OnSLP")
                await appStack[-1].on_sleep()
                
                # The modded micropython lets us sleep longer
                # Because an IRQ can cancel sleep
                endSleepOnSelPin=True
                #Check if we can turn off the wifi.
                checkOldWifi(False)
                print("Sleeping")
                time.sleep(0.010)
                
                try:
                    dstime = config.get('sleeptime',600)
                    dstime=dstime*1000
                except:
                    dstime = (10*60*1000)
                    
                if dstime and (wakeLock == 0):
                    if (time.ticks_diff(time.ticks_ms(),lastInteraction))> dstime:
                        print("Enter Deep Sleep")
                        try:
                            rtc.memory(json.dumps(rtc_ram).encode())
                        except Exception as e:
                            print("Failed to save RTC RAM state")
                            sys.print_exception(e)
                        
                        
                        machine.deepsleep(3600000)
                    
                #Must come BEFORE auto sleep, it would reset this
                machine.freq(min_cpu_freq)
                try:
                    machine.auto_sleep(True)
                    t = time.ticks_ms()
                    while selpin.value() and wakepin.value():
                        unlocked = False
                        
                        time.sleep(1)
                           

                        #Break due tinterrupt
                        if (time.ticks_diff(time.ticks_ms(),lastInteraction) <  1000):
                            break
                        
                        if time.ticks_diff(time.ticks_ms(),t) > 20000:
                            break
                    endSleepOnSelPin=False
                    machine.auto_sleep(False)
                    
                    while(selpin.value()==0 and wakepin.value()==0):
                        lastInteraction= time.ticks_ms()
                        time.sleep(0.05)
                except:
                    # Seems to crash if anything gets printed during low freq?
                    machine.freq(max_cpu_freq)
                    raise
                finally:
                   machine.freq(max_cpu_freq)
                machine.auto_sleep(False)
                
                print("Appwaketick")
                appTickRate = await appStack[-1].on_tick()
            else:
                if not tft_was_on:
                    print("ScreenWake")
                    tft.on()
                    doWifi()
                    tft.sleep_mode(0)
                    await appStack[-1].on_wake()
                    tft_was_on=True
                    
                if time.ticks_diff(time.ticks_ms(),lastTick) > appTickRate:
                    print("TICC")
                    appTickRate = await appStack[-1].on_tick() or 1000                 
                    lastTick = time.ticks_ms()
                
                #Set wifi in use timestampes
                checkOldWifi(True)
                

                machine.auto_sleep(True)
                time.sleep(0.041)
                machine.auto_sleep(False)
                
    except Exception as e:
        machine.freq(max_cpu_freq)
        print("EEERR")
        sys.print_exception(e)
        await card(None,"Err", [str(e)])
        time.sleep(1)
        machine.soft_reset()


def run(app):
    import uasyncio
    loop = uasyncio.get_event_loop()
    loop.run_until_complete(_run(app))