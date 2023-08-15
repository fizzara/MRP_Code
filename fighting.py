import cv2
import numpy as np
import tts
import findCheck
from PIL import Image
import pygame as pg


pg.init()
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]
while True:
    for event in pg.event.get():
        if event.type == pg.JOYBUTTONDOWN:
            print(event)



def fightingLoop():
    pass