from krevetka import *
from tkinter import *
from time import sleep
from online_sources import *
import os
tk = Tk()
tk.title("Chess")
tk.configure(cursor = "hand2")
w = Canvas(tk, width=640, height=640, bg="#ffffff")
w.pack()
Move = ""
phase = 0
lichess_url = None
def Undo():
    global coord
    try:
        coord.pop()
        coord.pop()
    except:
        pass
    Draw()


def select1():
    global phase, Btn1, Btn2, Btn3, undo
    enter.destroy()
    phase = 1
    Btn1.destroy()
    Btn2.destroy()
    Btn3.destroy()
    undo = Button(tk, text="undo", overrelief="ridge", command=Undo)
    undo.pack()
    Draw()


def select2():
    global phase, Btn1, Btn2, Btn3, undo, enter
    phase = 2
    Btn1.destroy()
    Btn2.destroy()
    Btn3.destroy()
    undo = Button(tk, text="undo", overrelief="ridge", command=Undo)
    undo.pack()
    enter.pack()
    Draw()


def select3():
    global phase, Btn1, Btn2, Btn3, undo, enter
    phase = 3
    Btn1.destroy()
    Btn2.destroy()
    Btn3.destroy()
    Draw()
    play_white(coord)
    undo = Button(tk, text="undo", overrelief="ridge", command=Undo)
    undo.pack()
    enter.pack()
    Draw()


def click(event):
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
                play_black(coord)
                Draw()
            elif phase == 3 and test != coord:
                play_white(coord)
                Draw()


def select_url(event):
    #lichess game
    global lichess_url, enter
    lichess_url = enter.get()
    enter.destroy()
    w.create_text(320, 320, text="5s for the mouse to be in the top left-hand corner of the board", fill="green", tag="url")
    tk.update()
    coord_board1 = get_mouse_board()
    w.itemconfigure("url", state="hidden")
    w.create_text(320, 320, text="5s for the mouse to be in the lower right-hand corner of the board", fill="green", tag="url")
    tk.update()
    coord_board2 = get_mouse_board()
    w.itemconfigure("url", state="hidden")
    coord_board = coord_board1+coord_board2
    old_data = []
    if phase == 3:
        play_mouse(str(coord.move_stack[-1]), coord_board, False)
    while True:
        if phase == 2:
            #si ia joue les noirs...
            data = lichess_board(lichess_url)
            #print(data)
            if len(data)%2!=0 and data!=old_data:
                #print(data[-1])
                play_human(data[-1])        
                Draw()
                old_data = data
                print("ia noir va jouer")
                play_black(coord)
                play_mouse(str(coord.move_stack[-1]), coord_board, coord.turn)
                Draw()
            else:
                print("en attente(le blancs doivent jouer)")
                #print(data)
                sleep(2)
        elif phase == 3:
            data = lichess_board(lichess_url)
            if len(data)%2==0 and data!=old_data:
                play_human(data[-1])
                Draw()
                old_data = data
                print("ia blanc va jouer")
                play_white(coord)
                play_mouse(str(coord.move_stack[-1]), coord_board, coord.turn)
                Draw()
            else:
                print("en attente(les noirs doivent jouer)")
            sleep(2)
        else:
            break

def Draw():
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

for i in range(1, 9, 2):  # creation du plateau en interface
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
#Btn4 = Button(tk, text="learn", overrelief="ridge", command=select4)
#Btn4.pack()
enter.bind("<Return>", select_url)
w.bind_all("<Button-1>", click)
tk.mainloop()
