# coding: utf-8

"""
Un module de gestion de l'écran que je reprends (un peu allégé) d'un ancien dépôt
d'Adafruit : https://github.com/adafruit/micropython-adafruit-rgb-display

À remplacer par quelque chose de plus actuel.

Largement hacké pour faire fonctionner les écrans que j'ai à ma disposition
actuellement :

- un 128x160 en red tab (languette rouge), uniquement pour tester car je souhaite 128x128
- un 128x128 en red tab 
- un 128x128 en green tab

Le green tab est celui qui donne les meilleurs résultats, mais l'offset qu'on 
paramètre avec CASET et RASET laisse toujour une ligne en « noise ».
J'ai trouvé un contournement pour ça mais il faudrait régler correctement le problème.

"""

from rgb import DisplaySPI, color565
import ustruct

_NOP=const(0x00)
_SWRESET=const(0x01)
_RDDID=const(0x04)
_RDDST=const(0x09)

_SLPIN=const(0x10)
_SLPOUT=const(0x11)
_PTLON=const(0x12)
_NORON=const(0x13)

_INVOFF=const(0x20)
_INVON=const(0x21)
_DISPOFF=const(0x28)
_DISPON=const(0x29)
_CASET=const(0x2A)
_RASET=const(0x2B)
_RAMWR=const(0x2C)
_RAMRD=const(0x2E)

_PTLAR=const(0x30)
_COLMOD=const(0x3A)
_MADCTL=const(0x36)

_FRMCTR1=const(0xB1)
_FRMCTR2=const(0xB2)
_FRMCTR3=const(0xB3)
_INVCTR=const(0xB4)
_DISSET5=const(0xB6)

_PWCTR1=const(0xC0)
_PWCTR2=const(0xC1)
_PWCTR3=const(0xC2)
_PWCTR4=const(0xC3)
_PWCTR5=const(0xC4)
_VMCTR1=const(0xC5)

_RDID1=const(0xDA)
_RDID2=const(0xDB)
_RDID3=const(0xDC)
_RDID4=const(0xDD)

_PWCTR6=const(0xFC)

_GMCTRP1=const(0xE0)
_GMCTRN1=const(0xE1)

_TEOFF=const(0x34)
_TEON=const(0x35)
_IDMOFF=const(0x38)
_IDMON=const(0x39)
_GAMSET=const(0x26)


class ST7735R(DisplaySPI):
    _COLUMN_SET = _CASET
    _PAGE_SET = _RASET
    _RAM_WRITE = _RAMWR
    _RAM_READ = _RAMRD
    _INIT = (
        (_SWRESET, None),
        (_SLPOUT, None),
        (_INVOFF, None),
        (_COLMOD, b'\x05'), # 16bit color
        (_DISPON, None),
        (_MADCTL, b'\x08'), # Sens, rotation
        # (_MADCTL, bytearray([0b01000100])), # bottom to top refresh
        (_DISSET5, b'\x15\x02'), 
        # (_FRMCTR1, b'\x06\x01\x00'), # 128x128 blue
        (_FRMCTR1, b'\x00\x00\x00'), # 128x160 et 128^2 green tab ABSOLUMENT NECESSAIRE POUR NE PAS AVOIR LES TRAITS NOIRS
        (_GAMSET, b'\x02'),
        (_GMCTRP1, b'\x09\x16\x09\x20\x21\x1b\x13\x19'
                   b'\x17\x15\x1e\x2b\x04\x05\x02\x0e'), # Gamma
        (_GMCTRN1, b'\x08\x14\x08\x1e\x22\x1d\x18\x1e'
                   b'\x18\x1a\x24\x2b\x06\x06\x02\x0f'),
    )

    def __init__(self, spi, dc, cs, rst=None, width=128, height=128):
        super().__init__(spi, dc, cs, rst, width, height)

    def init(self):
        super().init()
        cols = ustruct.pack('>HH', 0, self.width - 1)
        rows = ustruct.pack('>HH', 0, self.height - 1)
        for command, data in (
            (_NORON, None),
            (_DISPON, None),
        ):
            self._write(command, data)
