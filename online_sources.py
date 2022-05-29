from urllib.request import urlopen
from time import time, sleep
import pyautogui

def lichess_board(url):
    t = time()
    try:
        data = str(urlopen(url).read())
    except:
        print("UNE ERREUR S'EST PRODUITE")
        try:
            data = str(urlopen(url).read())
        except:
            import os
            try:
                os.system("urlliberror.mp3")
            except:
                pass
    if "draw" in data:
        data = data[data.find("1. "):data.find("{ The game is a draw. }")].split()
    elif "Black wins by" in data:
        data = data[data.find("1. "):data.find("{ Black wins by ")].split()
    elif "White wins by" in data:
        data = data[data.find("1. "):data.find("{ Black wins by ")].split()
    else:
        data = data[data.find("1. "):data.find("""*</div></div></aside><div class="round__board main-board">""")].split()
    real_data = []
    for moves in data:
        if not "." in moves:
            real_data.append(moves)
    #print(time()-t)
    return real_data

def syzygy(board_fen="4k3/8/8/8/8/3Q4/8/4K3 w"):
    try:
        board_fen = board_fen.replace(" ", "_")
        t = time()
        data = str(urlopen("https://syzygy-tables.info/?fen="+board_fen).read())
        data = data[data.find(" is "):data.find('<span class="badge">')]
        data = data[::-1]
        data = data[:data.find(">")]
        data = data[::-1]
        print("DATA:",data)
        #print(time()-t)
    except:
        data = ""
    return data

def get_mouse_board():
    print("vous avez 5s pour le coin")
    sleep(5)
    x, y = pyautogui.position()
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
    if not turn:
        startx = (alpha.find(start[0])+0.5)*dx+x1
        starty = y2 - (int(start[1])-0.5)*dy
        finishx = (alpha.find(finish[0])+0.5)*dx+x1
        finishy = y2 - (int(finish[1])-0.5)*dy
    else:
        startx = x2-((alpha.find(start[0])-0.5)*dx+x1)
        starty = y1+(int(start[1])-0.5)*dy
        finishx = x2-((alpha.find(finish[0])-0.5)*dx+x1)
        finishy = y1+(int(finish[1])-0.5)*dy
    pyautogui.click(startx, starty)
    pyautogui.click(finishx, finishy)

