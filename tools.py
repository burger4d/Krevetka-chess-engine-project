from urllib.request import urlopen
from time import time, sleep
from krevetka import *
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
    x, y = pyautogui.position()
    print("mouse",x, y)
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

def get_board(turn="white", game="lichess"):
    c = pyautogui.locateOnScreen("images/"+game+"/"+turn+"/board.png", confidence=0.4)
    return c

def get_move2(a, b, turn="white", game="lichess"):
    s = pyautogui.screenshot("board.png", (a[0], a[1], b[0]-a[0], b[1]-a[1]))
    onex = s.size[0]//8
    oney = s.size[1]//8
    moves = []
    pixel=None
    with open("images/"+game+"/pixel.txt", "r") as file:
        pixel=eval(file.read())
        file.close()
    print(pixel)
    for c in range(8):
        for d in range(8):
            p  = s.getpixel((c*onex+onex//2, d*oney+oney//20))
            #print(p, c, d)
            if p in pixel:
                print(c, d)
                moves.append((c, d))
    print(moves)
    if len(moves) == 2:
        start = moves[0]
        end = moves[1]
        alpha = "abcdefgh"
        num = 8
        if turn == "black":
            alpha=alpha[::-1]
            num = -1
        start = alpha[start[0]]+str(abs(num-start[1]))
        end = alpha[end[0]]+str(abs(num-end[1]))
        print(start, end)
        return [start, end]
    else:
        return["aa","bb"]


def get_move(a, b, turn="white", game="lichess"):
    im = pyautogui.screenshot("board.png", (a[0], a[1], b[0]-a[0], b[1]-a[1]))
    onex = im.size[0]//8
    oney = im.size[1]//8
    d = {}
    pixel=None
    with open("images/"+game+"/pixel.txt", "r") as file:
        pixel=eval(file.read())
        file.close()
    for x in range(8*onex):
        for y in range(8*oney):
            #print(x, y)
            rgb = im.getpixel((x, y))
            square = str(x//onex)+str(y//oney)
            if rgb in pixel:
                if square in d:
                    d[square] += 1
                else:
                    d[square] = 1
    squares = ["No", "No"]
    squares_val = [0, 0]
    print(d)
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
    #print(squares)
    start = squares[0]
    end = squares[1]
    alpha = "abcdefgh"
    num = 8
    if turn == "black":
        alpha = alpha[::-1]
        num = -1
    print(start, end)
    if not "No" in squares:
        start = alpha[int(start[0])]+str(abs(num-int(start[1])))
        end = alpha[int(end[0])]+str(abs(num-int(end[1])))
    print(start, end)
    return [start, end]


def get_fen(a, b, turn="white", game="lichess"):
    d = {"king": "k", "pawn": "p", "knight": "n", "queen":"q", "bishop":"b", "rook":"r"}
    c = {}
    for color in ["white", "black"]:
        for piece in ["empty", "king", "pawn", "knight", "queen", "bishop", "rook"]:
            l=[]
            board = pyautogui.locateAllOnScreen("images/"+game+"/"+color+"/"+piece+".png", confidence=0.7)
            for i in board:
                if i.top > a[1]:
                    l.append(i)
            l2=[]
            alpha = "abcdefgh"
            width = abs(a[0]-b[0])
            height = abs(a[1]-b[1])
            one = width//8
            for i in l:
                try:
                    nx = (i.left+one//2-a[0])//one
                    letter = alpha[nx]
                    ny = 8-(i.top+one//2-a[1])//one
                    case = letter+str(ny)
                except:
                    case = "42"
    #pyautogui.click(i.left, i.top)
                if case not in l2:
                    #print(nx, ny)
                #pyautogui.click(i.left, i.top)
                    l2.append(case)
                    #print(case)
            #print(color, piece, l2)
            for i in l2:
                if color == "white":
                    c[i] = d[piece].upper()
                else:
                    c[i] = d[piece]
    #print(c)
    fen = ""
    score = 0
    for i in range(8, 0, -1):
        for a in alpha:
            square = a+str(i)
            if square in c and square!="empty":
                if score!=0:
                    fen+=str(score)
                fen+=c[square]
                score=0
            else:
                score+=1
            if a == "h":
                if score!=0:
                    fen+=str(score)
                    score=0
                if i!=1:
                    fen+="/"
    if turn!= "white":
        fen = fen[::-1]
    #print(fen)
    return fen


def recognize_move(board, fen):
    d = {board.fen(): "nothing"}
    l = [board.fen()]
    for i in board.legal_moves:
        board2 = copy.copy(board)
        board2.push_san(str(i))
        d[board2.fen()]=str(i)
        l.append(board2.fen())
    pprint(d)
    print(fen)
    for i in l:
        if fen in i:
            return d[i]
    return d[process.extractOne(fen, l)[0]]
