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


def singleton(class_):
    """
    La classe [SMOL] représente la console, elle ne doit être instanciée qu'une seule fois.
    La fonction [singleton] est utilisée pour créer un singleton de la classe [SMOL] via decorator.

    Pour référence sur les singletons : 
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python/

    Habituellement j'utilise les metaclass pour ça, mais ce n'est pas disponible dans MicroPyton pour 
    le moment. Le problème avec les décorateurs c'est qu'il n'est pas possible d'utiliser des méthodes 
    statiques. À voir s'il est possible de faire autrement à l'avenir.
    """
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class SMOL:

    """
    On ne gère ici que la console SMOL, donc toutes les valeurs pour les pins sont en fixées.

    cs = 18
    rst = 5
    rs (dc) = 19
    sck = 14
    mosi = 13
    miso = 12

    """

    def __init__(self):

        self.spi = SPI(1, baudrate=59000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12)) 
        self.display = st7735.ST7735R(self.spi, dc=Pin(19), cs=Pin(18), rst=Pin(5), width=130, height=130)
        
        self.fb = framebuf.FrameBuffer(bytearray(130*130*2), 130, 130, framebuf.RGB565)
        self.fb.fill_rect(0, 0, 130, 130, black) # voir pour les valeurs 130 <-> 128

        self.display.fill(black)
        # À ce moment SMOL() affiche un écran noir.



    def make_sprite(self, sprite_filename, width, height):
        """
        Génère un buffer de sprite depuis un nom de fichier raw, retourne ce buffer.
        """
        with open(str(sprite_filename) + ".raw", "rb") as f:
            sprite_buf = f.read()
            return framebuf.FrameBuffer(bytearray(list(sprite_buf)), width, height, framebuf.RGB565)

    def draw_sprite(self, sprite, x, y):
        """
        Blit d'un buffer de sprite sur le framebuffer aux coordonnées précisées.
        """
        self.fb.blit(sprite, x, y)

    def draw(self):
        """
        Blit du framebuffer entier sur l'écran via SPI.
        """
        self.display.blit_buffer(self.fb, 0,0, 130,130)
            

