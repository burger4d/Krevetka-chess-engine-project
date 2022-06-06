from krevetka import *
from tkinter import *
from time import sleep
from online_sources import *
tk = Tk()
tk.title("Chess")
tk.configure(cursor = "hand2")
w = Canvas(tk, width=640, height=640, bg="#ffffff")
w.pack()
Move = ""
phase = 0
lichess_url = None
lvl = 0

def Undo():
    """undo a move"""
    global coord
    try:
        coord.pop()
    except:
        pass
    Draw()

def global_select():
    global Btn1, Btn2, Btn3, undo, lvl, level, enter, li_option
    Btn1.destroy()
    Btn2.destroy()
    Btn3.destroy()
    lvl = level.get()
    level.destroy()
    if IsLichessGame.get()=="on":
        enter.pack()
    li_option.destroy()
    undo = Button(tk, text="undo", overrelief="ridge", command=Undo)
    undo.pack()
    
def select1():
    """human vs human"""
    global phase, enter
    enter.destroy()
    global_select()
    phase = 1
    Draw()


def select2():
    """human(White) vs Ai(Black)"""
    global phase
    phase = 2
    global_select()
    Draw()


def select3():
    """AI(White) vs human(Black)"""
    global phase, lvl
    phase = 3 
    global_select()
    play_white(coord, lvl)
    Draw()

def select4():
    """for the tests"""
    global phase, Btn1, Btn2, Btn3, Btn4, lvl, level
    phase = 3
    Btn1.destroy()
    Btn2.destroy()
    Btn3.destroy()
    Btn4.destroy()
    lvl = level.get()
    level.destroy()
    while 1:
        Draw()
        play_white(coord, lvl)
        Draw()
        play_black(coord, lvl)
        

def click(event):
    """getting the position of the click and moving pieces"""
    global Move
    if phase != 0:
        Draw()
        test = copy.copy(coord)
        if phase != 3:
            x = "abcdefgh"[event.x // 80]
            y = str(8 - event.y // 80)
        else:
            x = "abcdefgh"[::-1][event.x // 80]
            y = str(-(-event.y//80))
        Move += x+y
        if phase != 3:
            x="abcdefgh".find(x)*80
            y=(8-int(y))*80
        else:
            x="abcdefgh"[::-1].find(x)*80
            y=(int(y)-1)*80
        w.create_oval(x+35, y+35, x+45, y+45, fill="red", tag="pieces")
        tk.update()
        if len(Move)==4:
            play_human(Move)
            play_human(Move+"q")
            Move = ""
            Draw()
            if phase == 2 and test != coord:
                play_black(coord, lvl)
                Draw()
            elif phase == 3 and test != coord:
                play_white(coord, lvl)
                Draw()


def select_url(event):
    """if this is a lichess game"""
    global lichess_url, enter
    lichess_url = enter.get()
    enter.destroy()
    sec=5
    while sec>0:
        w.create_text(320, 320, text=str(sec)+"s for the mouse to be in the\ntop left-hand\ncorner of the board", fill="green", font="Times 20", tag="url")
        tk.update()
        sleep(1)
        sec-=1
        w.itemconfigure("url", state="hidden")
    coord_board1 = get_mouse_board()
    sec=5
    while sec>0:
        w.create_text(320, 320, text=str(sec)+"s for the mouse to be in the\nlower right-hand\ncorner of the board", fill="green", font="Times 20", tag="url")
        tk.update()
        sleep(1)
        sec-=1
        w.itemconfigure("url", state="hidden")
    coord_board2 = get_mouse_board()
    coord_board = coord_board1+coord_board2
    old_data = []
    if phase == 3:
        play_mouse(str(coord.move_stack[-1]), coord_board, False)
    while True:
        if phase == 2:
            data = lichess_board(lichess_url)
            if len(data)%2!=0 and data!=old_data:
                play_human(data[-1])        
                Draw()
                old_data = data
                print("Krevetka(Black) is thinking")
                play_black(coord, lvl)
                play_mouse(str(coord.move_stack[-1]), coord_board, coord.turn)
                Draw()
            else:
                print("waiting(White must play)")
                sleep(1)
        elif phase == 3:
            data = lichess_board(lichess_url)
            if len(data)%2==0 and data!=old_data:
                play_human(data[-1])
                Draw()
                old_data = data
                print("Krevetka(White) is thinking...")
                play_white(coord, lvl)
                play_mouse(str(coord.move_stack[-1]), coord_board, coord.turn)
                Draw()
            else:
                print("waiting(Black must play)")
            sleep(1)
        else:
            break

def Draw():
    """'drawing' the board"""
    w.itemconfigure("pieces", state="hidden")
    d = string_coord(coord)
    if phase == 3:
        d=string_coord(coord)[::-1]
    for i in range(8):
        for j in range(8):
            w.create_text((j+0.5) * 80, (i + 0.5) * 80, text={".":" ", "K":chr(9812), "k":chr(9818),
                                                            "Q":chr(9813), "q":chr(9819), "R":chr(9814),
                                                            "r":chr(9820), "B":chr(9815), "b":chr(9821),
                                                            "N":chr(9816), "n":chr(9822), "P":chr(9817),
                                                            "p":chr(9823)}[d[i*8+j]], font="Times 50", tag="pieces")
    verification()
    tk.update()

def verification():
    """verify if there is a checkmate, a draw..."""
    global phase
    if coord.is_checkmate():
        phase = 0
        w.create_text(320, 360, text="checkmate", font="Times 30", fill="red")
        try:
            os.system("endgame.mp3")
        except:
            pass
    elif coord.is_stalemate():
        phase = 0
        w.create_text(320, 320, text="DRAW", font="Times 30", fill="orange")
        try:
            os.system("endgame.mp3")
        except:
            pass
    elif coord.can_claim_draw():
        w.create_text(320, 320, text="DRAW?", font="Times 30", fill="orange")

for i in range(1, 9, 2):  # the squares of the board
    for j in range(1, 9, 2):
        w.create_rectangle(i*80, (j-1)*80, (i+1)*80, j*80, fill="#cccccc")
for i in range(0, 9, 2):
    for j in range(0, 9, 2):
        w.create_rectangle(i*80, (j-1)*80, (i+1)*80, j*80, fill="#cccccc")
        
Draw()
w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
w.create_text(320, 320, text="/!\ WARNING:You shall not win.\nBut if you have some bravness,\nfight for the draw against one of the \nmost powerful and dynamic \nchess engine written in python:\nKrevetka"+chr(129424), font="Times 20", fill="red", tag="pieces")
Btn1 = Button(tk, text="human vs human", overrelief="ridge", command=select1)
Btn1.pack()
Btn2 = Button(tk, text="human vs AI", overrelief="ridge", command=select2)
Btn2.pack()
Btn3 = Button(tk, text="AI vs human", overrelief="ridge", command=select3)
Btn3.pack()
enter = Entry(tk)
#Btn4 = Button(tk, text="test", overrelief="ridge", command=select4)
#Btn4.pack()
IsLichessGame = StringVar()
li_option = Checkbutton(tk, text="Lichess Game", variable=IsLichessGame, onvalue="on", offvalue="off")
IsLichessGame.set("off")
li_option.pack()
level = Scale(tk, orient="horizontal", from_=0, to=3, resolution=1, tickinterval=10, length=100, label="level(depth)")
level.pack()
level.set(3)
enter.bind("<Return>", select_url)
w.bind_all("<Button-1>", click)
tk.mainloop()
