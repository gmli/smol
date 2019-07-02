# coding: utf-8

from smol import display, sprite

classroom = sprite("background", 128, 128)

display.draw_sprite(classroom, 0, 0)
display.refresh()

'''
display.refresh() -> soit ça envoi les données via SPI immédiatement, 
soit ça flag l'écran pour qu'un timer ait l'autorisation d'updater l'écran si x millisecondes sont passées.
Avec par exemple un display.set_max_fps(xx) qui donne les fps _maxi_.
Par contre avec le flag, peut-être qu'un triple buffering serait nécessaire -> tester si on a des problèmes de scintillement ou tearing.
'''
