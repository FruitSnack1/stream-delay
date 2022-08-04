from datetime import datetime
import os
import re
import signal
import sys
import threading
from time import sleep
from PIL import ImageEnhance
from pytesseract import pytesseract
import pyautogui
import tkinter as tk

HEIGHT = 300
WIDTH = 650
START_TIME = datetime.now().timestamp()
LOG_NAME = f'log{datetime.fromtimestamp(START_TIME)}.log'
SAVE_PREVIEW_IMG = True


window = tk.Tk()
window.title('')
window.resizable(width=False, height=False)

var = tk.StringVar()
var.set(str(datetime.now().timestamp()))

label = tk.Label(window, textvariable=var,
                 font=('Monospace', 40), padx=5, pady=5, background='white')
label.pack()
quitting = False


def takeScreenshot():
    screen = pyautogui.screenshot(
        region=(1920 * 2 - WIDTH, 1200 - HEIGHT, WIDTH, HEIGHT))
    if SAVE_PREVIEW_IMG:
        screen.save('./screenshot.png')
    return screen


def calculateDelay(img) -> float:
    text = getImageText(img)
    # filter characters
    result = re.sub(r'[^\d.]', '', text)
    print(result)
    if len(result) != 34:
        return -1
    return float(result[17:34]) - float(result[0:17])


def getImageText(img) -> str:
    img = img.convert('L')
    text = pytesseract.image_to_string(img)
    return text


def addSummary() -> None:
    seconds = round(datetime.now().timestamp() - START_TIME, 0)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    try:
        f = open(f'./logs/{LOG_NAME}', 'r')
        lines = f.readlines()
        delays = []
        for line in lines:
            delays.append(float(line[34:52]))
        f.close()
        f = open(f'./logs/{LOG_NAME}', 'a')
        f.write('\nSUMMARY:\n')
        f.write(f'Test time: {int(h)}:{int(m)}:{int(s)}\n')
        f.write(f'Min delay: {min(delays)} s\n')
        f.write(f'Avg delay: {avg(delays)} s\n')
        f.write(f'Max delay: {max(delays)} s\n')
        f.close()
    except Exception:
        pass


def avg(array: list) -> float:
    return sum(array) / len(array)


def quit(signal, frame) -> None:
    global quitting
    addSummary()
    quitting = True
    sys.exit(0)


def updateWindow():
    var.set('{:.6f}'.format(round(datetime.now().timestamp(), 6)))
    window.update_idletasks()


signal.signal(signal.SIGINT, quit)
if not os.path.exists('./logs'):
    os.makedirs('./logs')


def doStuff():
    while not quitting:
        screenshot = takeScreenshot()
        delay = calculateDelay(screenshot)
        if delay > 0 and delay < 15:
            print(f'current delay :{delay}')
            f = open(f'./logs/{LOG_NAME}', 'a')
            f.write(f'{datetime.now()} delay :{delay}\n')
            f.close()
        sleep(2)


if __name__ == "__main__":
    threading.Thread(target=doStuff).start()
    while True:
        updateWindow()
        curr = datetime.now().timestamp()
