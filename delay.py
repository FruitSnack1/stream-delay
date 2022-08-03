from datetime import datetime
import numpy as np
import cv2
from mss import mss
from PIL import Image
from termcolor import colored
import numpy as np
from colorama import Fore, Back, Style
import os
import pyautogui


colors = [Back.GREEN, Back.RED, Back.BLUE]
counter = 0
mon = {'left': 0, 'top': 200, 'width': 200, 'height': 200}
timestamp = datetime.now().timestamp()
changeTimestamp = datetime.now().timestamp()
currentDelay = 0
calculated = False
cameraColor = ''


def printSquare(col: str) -> None:
    for a in range(5):
        print(col + f"{currentDelay} {cameraColor}\n")
    print(Style.RESET_ALL)
    # os.system('clear')


def changeColor():
    global counter
    global timestamp
    global changeTimestamp, calculated
    changeTimestamp = datetime.now().timestamp()
    timestamp = curr
    counter = (counter + 1) % len(colors)
    calculated = True
    # printSquare(colors[counter])


with mss() as sct:
    while True:
        curr = datetime.now().timestamp()
        if curr - timestamp > 3:
            changeColor()

        screenShot = sct.grab(mon)
        img = Image.frombytes(
            'RGB',
            (screenShot.width, screenShot.height),
            screenShot.rgb,
        )
        cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        cv2.imshow('test', np.array(img))

        # setting values for base colors
        b = np.array(img)[:, :, :1]
        g = np.array(img)[:, :, 1:2]
        r = np.array(img)[:, :, 2:]

        # computing the mean
        b_mean = np.mean(b)
        g_mean = np.mean(g)
        r_mean = np.mean(r)

        print(r_mean)
        print(g_mean)
        print(b_mean)

        color = ''
        # displaying the most prominent color
        if ((b_mean > g_mean) and (b_mean > r_mean)):
            color = Back.BLUE
            cameraColor = 'blue'
            print('red')
        if ((g_mean > r_mean) and (g_mean > b_mean)):
            color = Back.GREEN
            cameraColor = 'green'
            print('green')
        if ((r_mean > b_mean) and (r_mean > g_mean)):
            color = Back.RED
            cameraColor = 'red'
            print('blue')

        if color == colors[counter] and not calculated:
            currentDelay = datetime.now().timestamp() - changeTimestamp
            calculated = True
        if cv2.waitKey(33) & 0xFF in (
            ord('q'),
            27,
        ):
            break
