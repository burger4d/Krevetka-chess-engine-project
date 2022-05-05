from krevetka import *
from tkinter import *
from time import sleep
tk = Tk()
tk.title("Chess")
tk.configure(cursor = "hand2")
w = Canvas(tk, width=640, height=640, bg="#ffffff")
w.pack()
Move = ""
phase = 0


def select1():
    global phase, Btn1, Btn2, Btn3
    phase = 1
    Btn1.destroy()
    Btn2.destroy()
    Btn3.destroy()
    Draw()
def select2():
    global phase, Btn1, Btn2, Btn3
    phase = 2
    Btn1.destroy()
    Btn2.destroy()
    Btn3.destroy()
    Draw()
def select3():
    global phase, Btn1, Btn2, Btn3
    phase = 3
    Btn1.destroy()
    Btn2.destroy()
    Btn3.destroy()
    Draw()
    play_white(coord)
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
                print(list_moves[-1])
                play_black(coord)
                Draw()
                print(list_moves[-1])
            elif phase == 3 and test != coord:
                print(list_moves[-1])
                play_white(coord)
                Draw()
                print(list_moves[-1])

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
    elif coord.is_stalemate() or coord.can_claim_draw():
        phase = 0
        w.create_text(320, 320, text="DRAW", font="Times 30", fill="orange")

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
#Btn4 = Button(tk, text="learn", overrelief="ridge", command=select4)
#Btn4.pack()
w.bind_all("<Button-1>", click)
tk.mainloop()
