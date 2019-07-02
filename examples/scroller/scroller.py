# coding: utf-8
from smol import display, sprite
from smol import RED, BLACK
from smol import left, right, button_a
from smol import collide_rect
import framebuf
import urandom
import utime



class Bullet(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.old_y = self.y

        self.sprite = framebuf.FrameBuffer(bytearray(2*6*2), 2, 6, framebuf.RGB565)
        self.sprite.fill_rect(int(0), int(0), 2, 6, RED)

    def update(self):
        self.y -= 5


class Bad(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.old_y = self.y
        self.sprite = sprite("bad", 8, 8)

    def update(self):
        if self.y > 128:
            self.y = 0
            self.x = urandom.getrandbits(6)
        self.y += 0.1


class BadManager(object):

    def __init__(self):
        self.bads = []
        self.counter = utime.ticks_ms()

    def _add_bad(self, bad):
        self.bads.append(bad)

    def update(self):
        if len(self.bads) < 3 and abs(utime.ticks_diff(self.counter, utime.ticks_ms())) > 1000:
            self.counter = utime.ticks_ms()
            bad = Bad(urandom.getrandbits(8), 0)
            
            # bad = Bad(20, 0)
            self._add_bad(bad)
        for bad in self.bads:
            bad.update()



manager = BadManager()


def user_moving():

    bullets = []
 
    x = 60
    y = 116
    old_x = x
    old_y = y
    move_x = 3
    move_y = 2

    player_size = 12#16#8
    player = sprite("player", player_size, player_size)

    player_erase = framebuf.FrameBuffer(bytearray(player_size*player_size*2), 
                                        player_size, player_size, framebuf.RGB565)
    player_erase.fill_rect(int(0), int(0),
                           player_size,player_size, BLACK)

    button_a_unpressed = False

    while True:
        display.clear()

        manager.update()

        old_x = x
        old_y = y
        if right():
            x += move_x
            x = min(x, 120)
        if left():
            x -= move_x
            x = max(x, 0)

        if button_a() and button_a_unpressed:
            button_a_unpressed = False
            new_bullet = Bullet(x+int(player_size/2)-1, y-6)
            bullets.append(new_bullet)
        if not button_a():
            button_a_unpressed = True
      
     
        # fb.blit(player_erase, old_x, old_y) # pas besoin si fb.fill(0) au début
        display.draw_sprite(player, x, y) 
        for bullet in bullets:
            bullet.update()
            if bullet.y < 0:
                bullets.remove(bullet)
                continue

            display.draw_sprite(bullet.sprite, bullet.x, bullet.y)
            for bad in manager.bads:
                if collide_rect(pad_x=bullet.x-1,pad_y=bullet.y,pad_width=4,pad_height=8,
                  player_x=bad.x,player_y=bad.y,player_width=8,player_height=8):
                  bad.y = 200
                  bullets.remove(bullet)
                  break



            
        for bad in manager.bads:
            bad.update()
            display.draw_sprite(bad.sprite, int(bad.x), int(bad.y), 0)
        # fb.blit(bullet, x+int(player_size/2)-1, y-6) 
        display.refresh()



        utime.sleep_ms(5)

user_moving()