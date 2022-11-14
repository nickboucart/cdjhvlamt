import random
import utime
import st7789
import tft_config
import vga1_16x16 as font


class Display:
    
    def __init__(self):
        self.tft = tft_config.config(1)
        self.tft.init()
        
    def center(self, text):
        self.clear_screen()
        length = len(text)
        self.tft.text(
            font,
            text,
            self.tft.width() // 2 - length // 2 * font.WIDTH,
            self.tft.height() // 2 - font.HEIGHT)
    
    def _text(self, text, x=0, y=0):
        self.tft.text(
            font,
            text,
            x,y)
    
    def text(self, txt):
        self.clear_screen()
        text_lines = self.split_string(txt)
        for i, text_line in enumerate(text_lines):
            self._text(text_line, y= i*font.HEIGHT)
        
    
    def clear_screen(self):
        self.tft.fill(st7789.BLACK)
        

    def split_string(self, str, sep=" "):
        limit = self.tft.width() // 16  # gehele deling - font is 16px breed, dit zoekt max aantal characters per schermlijn
        words = str.split()
#         if max(map(len, words)) > limit:
#             raise ValueError("limit is too small")
        res, part, others = [], words[0], words[1:]
        for word in others:
            if len(sep)+len(word) > limit-len(part):
                res.append(part)
                part = word
            else:
                part += sep+word
        if part:
            res.append(part)
        return res
