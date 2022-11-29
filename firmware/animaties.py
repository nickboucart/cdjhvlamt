import gc
import machine
try:
    import uasyncio as asyncio
except ImportError:
    import asyncio

import trickLED as tl
gc.collect()

from trickLED import animations32
from trickLED import animations
gc.collect()

class AnimatieMgr:
    
    def __init__(self, pin, aantalLeds):
        self.leds = tl.TrickLED(machine.Pin(33), aantalLeds)
        self.animation = None   
    
    def stop_annimation_and_run_new_one(self, animation_name):
        if self.animation:
            self.animation.stop()
        if animation_name == "fire":
            self.animation = tl.animations32.Fire(self.leds, interval=40)
            asyncio.create_task(self.animation.play(0, sparking=64, cooling=7, scroll_speed=2))
        elif animation_name == "conjunction":
            self.animation = tl.animations32.Conjunction(self.leds)
            asyncio.create_task(self.animation.play(0))
        elif animation_name == "sidesweep":
            self.animation = tl.animations.SideSwipe(self.leds)
            asyncio.create_task(self.animation.play(0))
        elif animation_name == "divergent":
            self.animation = tl.animations.Divergent(self.leds)
            asyncio.create_task(self.animation.play(0))
        elif animation_name == "jitter":
            self.animation = tl.animations.Jitter(self.leds)
            asyncio.create_task(self.animation.play(0))
        else:
            self.animation = tl.animations32.Fire(self.leds, interval=40)
            asyncio.create_task(self.animation.play(0, sparking=64, cooling=7, scroll_speed=2))
            



        gc.collect()
        
    
        
        
        
        