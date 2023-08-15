import pyfirmata
import keyboard
import time
from pyfirmata import Arduino, util
board = pyfirmata.Arduino('COM4')

if keyboard.is_pressed('1'):
    board.digital[3].write(1)
    time.sleep(0.5)
    board.digital[3].write(0)
if keyboard.is_pressed('2'):
    board.digital[4].write(1)
    time.sleep(0.5)
    board.digital[4].write(0)
if keyboard.is_pressed('3'):
    board.digital[5].write(1)
    time.sleep(0.5)
    board.digital[5].write(0)
if keyboard.is_pressed('4'):
    board.digital[6].write(1)
    time.sleep(0.5)
    board.digital[6].write(0)

