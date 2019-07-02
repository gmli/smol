# coding: utf-8

"""
Module principal pour la console SMOL.

Gère l'écran, les boutons, etc.

"""

import st7735
import rgb
import framebuf
from machine import Pin, SPI, Signal


black = rgb.color565(0,0,0)

spi = SPI(1, baudrate=59000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12)) 
framebuffer = framebuf.FrameBuffer(bytearray(130*130*2), 130, 130, framebuf.RGB565)
framebuffer.fill_rect(0, 0, 130, 130, black) # voir pour les valeurs 130 <-> 128

class Display(st7735.ST7735R):

    def __init__(self):
        super().__init__(spi, dc=Pin(19), cs=Pin(18), rst=Pin(5), width=130, height=130)

    def draw_sprite(self, sprite, x, y):
        framebuffer.blit(sprite, x, y)

    def refresh(self):
        self.blit_buffer(framebuffer, 0,0, 130,130)

display = Display()
display.fill(black)


def sprite(sprite_filename, width, height):
        """
        Génère un buffer de sprite depuis un nom de fichier raw, retourne ce buffer.
        """
        with open(str(sprite_filename) + ".raw", "rb") as f:
            sprite_buf = f.read()
            return framebuf.FrameBuffer(bytearray(list(sprite_buf)), width, height, framebuf.RGB565)


