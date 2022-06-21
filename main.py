from krevetka import *
from tkinter import *
from time import sleep
from tools import *
import sys

tk = Tk()
tk.title("Chess")
tk.configure(cursor = "hand2")
w = Canvas(tk, width=640, height=640, bg="#"+str(hex(239))[2:]+str(hex(216)[2:]+str(hex(181))[2:]))
w.pack()

mode = "start"  # start:nothing, normal:human vs human, play:AI vs human, bot: AI/you vs another person
click_move = ""  # the squares where you click
player = "white"
engine = None  # 'None' in the normal mode
book = "Nothing"  # name of the polyglot opening book choosen

for i in range(1, 9, 2):  # the squares of the board
    for j in range(1, 9, 2):
        w.create_rectangle(i*80, (j-1)*80, (i+1)*80, j*80, fill="#"+str(hex(181))[2:]+str(hex(136))[2:]+str(hex(99))[2:])

for i in range(0, 9, 2):
    for j in range(0, 9, 2):
        w.create_rectangle(i*80, (j-1)*80, (i+1)*80, j*80, fill="#"+str(hex(181))[2:]+str(hex(136))[2:]+str(hex(99))[2:])


def verification():
    """verify if there is a checkmate, a draw..."""
    global phase
    if coord.is_checkmate():
        phase = 0
        w.create_text(320, 360, text="checkmate", font="Times 30", fill="red")
        if engine not in [None, "Krevetka"]:
            try:
                engine.quit()
            except:
                pass
        if music:
            try:
                os.system("endgame.mp3")
            except:
                pass
        Btn = Button(tk, text="Back to the menu", command=menu)
        Btn.pack()
    elif coord.is_stalemate():
        phase = 0
        w.create_text(320, 320, text="DRAW", font="Times 30", fill="orange")
        if engine not in [None, "Krevetka"]:
            try:
                engine.quit()
            except:
                pass
        if music:
            try:
                os.system("endgame.mp3")
            except:
                pass
        Btn = Button(tk, text="Back to the menu", command=menu)
        Btn.pack()
    elif coord.can_claim_draw():
        w.create_text(320, 320, text="DRAW?", font="Times 30", fill="orange")


def Draw(turn):
    """'drawing' the board"""
    tk.title("Chess")
    tk.attributes("-topmost", -1)
    w.itemconfigure("pieces", state="hidden")
    d = string_coord(coord)  # from krevetka.py
    if turn != "white":
        d = d[::-1]
    for i in range(8):
        for j in range(8):
            D=d[i*8+j]
            if D == D.lower():
                w.create_text((j+0.5) * 80, (i + 0.5) * 80, text={".":" ", "k":chr(9818), "q":chr(9819),
                                                            "r":chr(9820), "b":chr(9821), "n":chr(9822),
                                                            "p":chr(9823)}[d[i*8+j]], font="Times 40", tag="pieces")
            else:
                w.create_text((j+0.5) * 80, (i + 0.5) * 80, text={".":" ", "k":chr(9818), "q":chr(9819),
                                                            "r":chr(9820), "b":chr(9821), "n":chr(9822),
                                                            "p":chr(9823)}[d[i*8+j].lower()], font="Times 40", fill="#666666", tag="pieces")
    verification()
    tk.update()


def menu():
    """quit the game and start again the programm"""
    file = __file__[::-1]
    file = file[:file.find("\\")][::-1]
    print(file)
    if sys.platform == "win32":
        os.system("start "+file)
    else:
        os.system("./"+file)
    quit()


def select0():
    """in all cases"""
    global Btn1, Btn2, click_move, music_opt, music
    Btn1.destroy()
    Btn2.destroy()
    Draw(player)
    click_move = ""
    try:
        music = MusicOption.get()=="on"  # boolean
        music_opt.destroy()
    except:
        pass


def select1():
    """human vs human"""
    global mode
    mode = "normal"
    select0()


def select2():
    """using AI"""
    global btn, variable, opt
    select0()
    w.create_text(320, 320, text="Choose the chess engine", font="Times 20", fill="green", tag="pieces")
    variable = StringVar()
    variable.set("Krevetka")
    engines = ["Krevetka"]
    if "engines" in os.listdir():
        engines += os.listdir("engines/"+sys.platform)
    opt = OptionMenu(tk, variable, *engines)
    opt.pack()
    btn = Button(tk, text="ok", command=select3)
    btn.pack()


def select3():
    """using AI -> ok"""
    global btn, engine, opt, Btn1, Btn2, level
    btn.destroy()
    opt.destroy()
    Draw(player)
    engine = variable.get()
    if engine == "Krevetka":
        level = Scale(tk, orient="horizontal", from_=0, to=3, resolution=1, tickinterval=10, length=100, label="level(depth)")
        level.pack()
        level.set(3)
    else:
        name = "engines/"+sys.platform+"/"
        print(name+engine)
        engine = chess.engine.SimpleEngine.popen_uci(name+engine)
    Btn1 = Button(tk, text="White vs AI", command=select4)
    Btn1.pack()
    Btn2 = Button(tk, text="AI vs Black", command=select3b)
    Btn2.pack()


def select3b():
    """using AI -> ok -> black"""
    global player
    player = "black"
    select4()


def select4():
    """using AI -> ok -> white or black"""
    global Btn1, Btn2, level, lvl, opt, variable
    try:
        lvl = level.get()
        level.destroy()
    except:
        pass
    select0()
    w.create_text(320, 320, text="About the chess engine...\n(Don't forget to choose\nif you want an opening book)", font="Times 20", fill="green", tag="pieces")
    books = ["Nothing"]
    if "polyglot" in os.listdir():
        books += os.listdir("polyglot")
    variable.set("Nothing")
    opt = OptionMenu(tk, variable, *books)
    opt.pack()
    Btn1 = Button(tk, text="play against it", command=select4p)
    Btn1.pack()
    Btn2 = Button(tk, text="use it as a bot", command=select4b)
    Btn2.pack()


def select4p():
    """using AI -> ok -> white or black -> play against it"""
    global mode
    mode = "play"
    select5()

    
def select4b():
    """using AI -> ok -> white or black -> use it as a bot"""
    global mode
    mode = "bot"
    select5()


def select5():
    """using AI -> ok -> white or black -> play against it or use it as a bot"""
    global engine, btn, opt, book, variable
    book = variable.get()
    opt.destroy()
    select0()
    w.create_text(320, 320, text="Choose the website", font="Times 20", fill="green", tag="recognition")
    if mode == "bot":
        websites = []
        if "images" in os.listdir():
            websites += os.listdir("images")
        variable.set(websites[0])
        opt = OptionMenu(tk, variable, *websites)
        opt.pack()
        btn = Button(tk , text="ok", command=select6)
        btn.pack()
    else:
        w.create_text(320, 320, text="Double-Click anywhere to start", font="Times 20", fill="green", tag="pieces")


def select6():
    """using AI -> ok -> white or black -> use it as a bot -> ok"""
    w.itemconfigure("recognition", state="hidden")
    global btn, website, opt, player2
    btn.destroy()
    website = variable.get()
    opt.destroy()
    player2 = "white"  # player: user, player: AI/Bot
    if player == "white":
        player2 = "black"
    print(player2, website)
    bot()
    

def bot():
    """bot is coming..."""
    #BoardPos = get_board(player2, website)
    #print(BoardPos, website)
    if 1==2:#BoardPos != None and website != "chess.com":  # if board found with image recognition
        coord_board1 = [BoardPos.left, BoardPos.top]
        coord_board2 = [BoardPos.left+BoardPos.width, BoardPos.top+BoardPos.height]
    else:  # if not found with image recognition, use the mouse to detect the corners
        sec = 5
        while sec>0:
            w.create_text(320, 320, text=str(sec)+"s for the mouse to be in the\ntop left-hand\ncorner of the board", fill="red", font="Times 20", tag="recognition")
            tk.update()
            sleep(1)
            sec-=1
            w.itemconfigure("recognition", state="hidden")
        coord_board1 = get_mouse_board()
        coord_board1[1]-=5
        sec = 5
        while sec>0:
            w.create_text(320, 320, text=str(sec)+"s for the mouse to be in the\nlower right-hand\ncorner of the board", fill="red", font="Times 20", tag="recognition")
            tk.update()
            sleep(1)
            sec-=1
            w.itemconfigure("recognition", state="hidden")
        coord_board2 = get_mouse_board()
    coord_board = coord_board1+coord_board2
    print(coord_board)
    if player2 == "white":
        if engine == "Krevetka":
            play_white(coord, lvl, book)
        else:
            play_engine(coord, engine, book)
        Draw(player)
        play_mouse(str(coord.move_stack[-1]), coord_board, player2=="black")
    while True:
        if coord.is_checkmate():
            break
        if (coord.turn and player == "white") or (not coord.turn and player == "black"):  # player's turn
            #fen = get_fen(coord_board1, coord_board2, player2, website)
            #move = recognize_move(coord, fen)
            move0 = get_move(coord_board1, coord_board2, player2, website)
            move1 = move0[0]+move0[1]  # e2e4 ?
            move2 = move0[1]+move0[0]  # or e4e2 ?
            l = list(map(str, coord.legal_moves))
            if move1 in l:
                move = move1
            elif move2 in l:
                move = move2
            else:
                if "e1h1" in [move1, move2] and "e1g1" in l:
                    move="e1g1"
                if "e8h8" in [move1, move2] and "e8g8" in l:
                    move="e8g8"
                move = "nothing"
            print("move", move)
            if move == "nothing":
                sleep(1)
            else:
                play_human(move)
                Draw(player)
        else:  # bot's turn
            if engine == "Krevetka":
                if player2 == "white":
                    play_white(coord, lvl, book)
                else:
                    play_black(coord, lvl, book)
            else:
                play_engine(coord, engine, book)
            play_mouse(str(coord.move_stack[-1]), coord_board, player2=="black")
            Draw(player)

def click(event):
    """getting the position of the click and moving pieces"""
    global click_move, player
    if mode != "start":
        if player == "white":
            x = "abcdefgh"[event.x // 80]  # converting the position of the mouse in the square
            y = str(8 - event.y // 80)
        else:
            x = "abcdefgh"[::-1][event.x // 80]
            y = str(-(-event.y // 80))
        click_move += x + str(y)  # adding the new square
        if len(click_move) == 4:  # like 'e2e4' and not just 'e2'
            play_human(click_move)
            play_human(click_move+"q")  # promoting by default the queen for the player
            click_move = ""  # avoiding the situation 'e2e4e7'
            Draw(player)
            if mode == "normal":
                if coord.turn and mode == "normal":  #switching the point of view
                    player = "white"
                if not coord.turn and mode == "normal":
                    player = "black"
            elif mode == "play":
                if player == "white" and not coord.turn:
                    if engine == "Krevetka":
                        play_black(coord, lvl, book)
                    else:
                        play_engine(coord, engine, book)
                if player == "black" and coord.turn:
                    if engine == "Krevetka":
                        play_white(coord, lvl, book)
                    else:
                        play_engine(coord, engine, book)
                verification()
                #Draw(player)
            Draw(player)
        else:
            if player == "white":
                x = "abcdefgh".find(x) * 80  # find the position where the oval can be drawed
                y = (8-int(y)) * 80
            else:
                x = "abcdefgh"[::-1].find(x) * 80
                y = (int(y)-1) * 80
            w.create_oval(x+35, y+35, x+45, y+45, fill="red", tag="pieces")
            tk.update()


w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
w.create_text(320, 320, text="/!\ WARNING:You shall not win.\nBut if you have some bravness,\nfight for the draw against one of the \nmost powerful and dynamic \nchess engine written in python:\nKrevetka"+chr(129424), font="Times 20", fill="red", tag="pieces")
MusicOption = StringVar()
music_opt = Checkbutton(tk, text="music option (plays a song when it is the end of the game)", variable=MusicOption, onvalue="on", offvalue="off")
MusicOption.set("off")
music_opt.pack()
Btn1 = Button(tk, text="human vs human", overrelief="ridge", command=select1)
Btn1.pack()
Btn2 = Button(tk, text="against AI", overrelief="ridge", command=select2)
Btn2.pack()
w.bind_all("<Button-1>", click)
tk.mainloop()
