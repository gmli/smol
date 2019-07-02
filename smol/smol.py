# coding: utf-8

"""
Module principal pour la console SMOL.

Gère l'écran, les boutons, etc.

"""

import st7735
import rgb
import framebuf
from machine import Pin, SPI, Signal


BLACK = rgb.color565(0,0,0)
RED = rgb.color565(255,0,0)

spi = SPI(1, baudrate=59000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12)) 
framebuffer = framebuf.FrameBuffer(bytearray(130*130*2), 130, 130, framebuf.RGB565)
framebuffer.fill_rect(0, 0, 130, 130, BLACK) # voir pour les valeurs 130 <-> 128

left  = Signal(4, Pin.IN, Pin.PULL_UP, invert=True)
right = Signal(15, Pin.IN, Pin.PULL_UP, invert=True)
button_a = Signal(22, Pin.IN, Pin.PULL_UP, invert=True)

class Display(st7735.ST7735R):

    def __init__(self):
        super().__init__(spi, dc=Pin(19), cs=Pin(18), rst=Pin(5), width=130, height=130)

    def draw_sprite(self, sprite, x, y, transparency_color=-1):
        framebuffer.blit(sprite, x, y, transparency_color)

    def clear(self):
        framebuffer.fill(0)

    def refresh(self):
        self.blit_buffer(framebuffer, 0, 0, 130, 130)

display = Display()
display.fill(BLACK)


def sprite(sprite_filename, width, height):
        """
        Génère un buffer de sprite depuis un nom de fichier raw, retourne ce buffer.
        """
        with open(str(sprite_filename) + ".raw", "rb") as f:
            sprite_buf = f.read()
            return framebuf.FrameBuffer(bytearray(list(sprite_buf)), width, height, framebuf.RGB565)


def collide_rect(pad_x,pad_y,pad_width,pad_height,
                  player_x,player_y,player_width,player_height):

    if (float(pad_x) < float(player_x) + float(player_width) and
            float(pad_x) + float(pad_width) > float(player_x) and
            float(pad_y) < float(player_y) + float(player_height) and
            float(pad_height) + float(pad_y) > float(player_y)):
        return True
    else:
        return False