from urllib.request import urlopen
from time import time, sleep
from krevetka import *
import pyautogui
from random import *
'''
from vosk import Model, KaldiRecognizer
import pyaudio

from fuzzywuzzy import process

model = Model("vosk-model-small-fr-0.22")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()


def recognize_audio():
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    text = "1"*20
    print("start")
    words = [""]
    while text[14:-3]!="":
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            print(text[14:-3])
            words.append(text[14:-3])
    return words[-2]

def get_part_of_move(is_number):
    List = ["a", "b", "c", "d", "e", "f", "g", "h"]
    if is_number:
        List = ["un", "deux", "trois", "six", "sept", "huit"]
    return process.extract(recognize_audio(), List)[0][0]
'''


def get_mouse_board():
    x, y = pyautogui.position()
    print("mouse", x, y)
    return [x, y]


def play_mouse(move, coord_mouse, turn):
    x1 = coord_mouse[0]
    y1 = coord_mouse[1]
    x2 = coord_mouse[2]
    y2 = coord_mouse[3]
    dx = abs(x1-x2)//8
    dy = abs(y1-y2)//8
    alpha = "abcdefgh"
    start = move[:2]
    finish = move[2:]
    startx = (alpha.find(start[0])+0.5)*dx+x1
    starty = y2 - (int(start[1])-0.5)*dy
    finishx = (alpha.find(finish[0])+0.5)*dx+x1
    finishy = y2 - (int(finish[1])-0.5)*dy
    if turn:
        startx = x2-startx+x1
        starty = y1+(int(start[1])-0.5)*dy
        finishx = x2-finishx+x1
        finishy = y1+(int(finish[1])-0.5)*dy
    pyautogui.click(startx, starty)
    pyautogui.click(finishx, finishy)
    if len(move) == 5:
        pyautogui.click()


def get_move(a, b, turn="white", game="chess.com"):
    im = pyautogui.screenshot("board.png", (a[0], a[1], b[0]-a[0], b[1]-a[1]))
    onex = im.size[0]//8
    oney = im.size[1]//8
    d = {}
    pixel = pixel2 = None
    with open("images/"+game+"/pixel.txt", "r") as file:
        pixel = eval(file.readline())
        pixel2 = eval(file.readline())
        file.close()
    for x in range(8*onex):
        for y in range(8*oney):
            rgb = im.getpixel((x, y))
            square = str(x//onex)+str(y//oney)
            if rgb in pixel:
                if square in d:
                    d[square] += 1
                else:
                    d[square] = 1
    squares = ["No", "No"]
    squares_val = [0, 0]
    for x in range(8):
        for y in range(8):
            square = str(x)+str(y)
            if square in d:
                val = d[square]
                if val > squares_val[0]:
                    squares_val = [val, squares_val[0]]
                    squares = [square, squares[0]]
                elif val > squares_val[1]:
                    squares_val = [squares_val[0], val]
                    squares = [squares[0], square]
    start = squares[0]
    end = squares[1]
    alpha = "abcdefgh"
    num = 8
    if turn == "black":
        alpha = alpha[::-1]
        num = -1
    if "No" not in squares:
        start = alpha[int(start[0])]+str(abs(num-int(start[1])))
        end = alpha[int(end[0])]+str(abs(num-int(end[1])))
    print(start, end)
    return [start, end]


def find_first_pixel(website):
    im = pyautogui.screenshot()
    with open("images/"+website+"/pixel.txt", "r") as f:
        f.readline()
        pixel2=eval(f.readline())
        f.close()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            rgb = im.getpixel((x, y))
            if rgb in pixel2:
                return [x, y]
    raise TypeError


def find_last_pixel(website):
    im = pyautogui.screenshot()
    with open("images/"+website+"/pixel.txt", "r") as f:
            f.readline()
            pixel2=eval(f.readline())
            f.close()
    for y in range(im.size[1]-1, 0, -1):
        for x in range(im.size[0]-1, 0, -1):
            rgb = im.getpixel((x, y))
            if rgb in pixel2:
                return [x, y]
    raise TypeError


def write_move(move):
    pyautogui.write(move)
