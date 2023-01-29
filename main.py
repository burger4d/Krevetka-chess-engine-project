from krevetka import *
from tkinter import *
from time import sleep, time
from tools import *
import sys
import pyttsx3

option_sound = True
voice = pyttsx3.init()


def speak(text):
    global engine
    if option_sound:
        voice.say(text)
        voice.runAndWait()


def verification(coord):
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
        Btn = Button(tk, text="Back to the menu", command=main)
        Btn.pack()
    elif coord.can_claim_draw():
        w.create_text(320, 320, text="DRAW?", font="Times 30", fill="orange", tag="pieces")


def Draw(turn):
    """'drawing' the board"""
    global last_move
    if engine==None:
        tk.title("Chess: "+mode+" mode")
    else:
        if coord.move_stack!=[]:
            tk.title("Chess: "+mode+" "+Engine+" "+str(coord.move_stack[-1]))
        else:
            tk.title("Chess: "+mode+" "+Engine)
    tk.attributes("-topmost", -1)
    w.itemconfigure("pieces", state="hidden")
    d = string_coord(coord)  # from krevetka.py
    if turn != "white":
        d = d[::-1]
    for i in range(8):
        for j in range(8):
            D=d[i*8+j]
            if D == D.lower():
                w.create_text((j+0.5) * 80,
                              (i + 0.5) * 80,
                              text={
                                  ".":" ", "k":chr(9818),
                                  "q":chr(9819),
                                  "r":chr(9820), "b":chr(9821),
                                  "n":chr(9822),
                                  "p":chr(9823)
                                  }[d[i*8+j]],
                              font="Times 40",
                              tag="pieces")
            else:
                w.create_text((j+0.5) * 80,
                              (i + 0.5) * 80,
                              text={
                                  ".":" ",
                                  "k":chr(9818),
                                  "q":chr(9819),
                                  "r":chr(9820),
                                  "b":chr(9821),
                                  "n":chr(9822),
                                  "p":chr(9823)
                                  }[d[i*8+j].lower()],
                              font="Times 40",
                              fill="#666666",
                              tag="pieces")
    verification(coord)
    if coord.move_stack!=[] and last_move!=coord.move_stack[-1] and music:
        speak(coord.move_stack[-1])
        last_move=coord.move_stack[-1]
    tk.update()


def select0():
    """in all cases"""
    global label, Btn1, Btn2, click_move, music_opt, music, textFen, fen_starter, coord
    try:
        label.destroy()
    except Exception as err:
        print(err)
    try:
        fen_starter = textFen.get()
        coord.set_board_fen(fen_starter)
        textFen.destroy()
    except Exception as err:
        print("invalide fen+"+str(err))
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
    global mode, ok
    ok=True
    Btn = Button(tk, text="Back to the menu", command=main)
    Btn.pack()
    mode = "normal"
    select0()


def select2():
    """using AI"""
    global btn, variable, opt
    select0()
    w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
    w.create_text(320, 320, text="Choose the chess engine", font="Times 20", fill="green", tag="pieces")
    variable = StringVar()
    variable.set("Krevetka")
    engines = ["Krevetka"]
    if "engines" in os.listdir():
        list_engines = []
        for file in os.listdir("engines/"+sys.platform):
            if (".dll" in file) or (".pb" in file):
                pass
            else:
                list_engines.append(file)
        engines += list_engines
    opt = OptionMenu(tk, variable, *engines)
    opt.pack()
    btn = Button(tk, text="ok", command=select3)
    btn.pack()


def select3():
    """using AI -> ok"""
    global btn, engine, opt, Btn1, Btn2, Btn3, level, Engine, time_thinking, engine_opt, EngineOption
    btn.destroy()
    opt.destroy()
    Draw(player)
    w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
    Engine = variable.get()
    if Engine == "Krevetka":
        engine="Krevetka"
        level = Scale(tk, orient="horizontal",
                      from_=0,
                      to=3,
                      resolution=1,
                      tickinterval=10,
                      length=100,
                      label="level(depth)")
        level.pack()
        level.set(2)
    else:
        """
        EngineOption = StringVar()
        engine_opt = Checkbutton(tk,
                            text="play by depth instead of time",
                            variable=EngineOption,
                            onvalue="on",
                            offvalue="off")
        EngineOption.set("on")
        engine_opt.pack()
        
        if time_is_depth:
            time_thinking = Scale(tk, orient="horizontal", from_=1, to=50, resolution=1, tickinterval=5, length=500, label="depth")
            time_thinking.set(5)
            time_thinking.pack()
        else:
            time_thinking = Scale(tk, orient="horizontal", from_=0.1, to=10, resolution=0.1, tickinterval=1, length=400, label="time thinking")
            time_thinking.set(1)
            time_thinking.pack()
        """
        name = "engines/"+sys.platform+"/"
        engine = chess.engine.SimpleEngine.popen_uci(name+Engine)
    w.create_text(320, 320, text="About the chess engine...", font="Times 20", fill="green", tag="pieces")
    Btn1 = Button(tk, text="play against it", command=select3p)
    Btn1.pack()
    Btn2 = Button(tk, text="use it as a bot", command=select3b)
    Btn2.pack()
    if engine!="Krevetka":
        Btn3 = Button(tk, text="chess board analysis", command=select3a)
        Btn3.pack()
        if time_is_depth:
            time_thinking = Scale(tk, orient="horizontal", from_=1, to=50, resolution=1, tickinterval=5, length=500, label="depth")
            time_thinking.set(5)
            time_thinking.pack()
        else:
            time_thinking = Scale(tk, orient="horizontal", from_=0.1, to=10, resolution=0.1, tickinterval=1, length=400, label="time thinking")
            time_thinking.set(1)
            time_thinking.pack()

def select3b():
    """using AI -> ok -> bot"""
    global mode
    mode = "bot"
    select4()


def select3p():
    """using AI -> ok -> play"""
    global mode
    mode = "play"
    print(1)
    select4()


def select3a():
    """using AI -> ok -> analysis"""
    global mode, Btn3, ok
    ok = True
    mode = "analysis"
    Btn3.destroy()
    select4()
    Undo = Button(tk, text="undo", command=undo)
    Undo.pack()
    Analyse = Button(tk, text="analyse", command=analyse)
    Analyse.pack()


def select4():
    """using AI -> ok -> bot or play"""
    global Btn1, Btn2, Btn3, level, lvl, opt, variable, time_thinking, time2think, engine_opt
    if engine!="Krevetka":
        pass
        time2think = time_thinking.get()
        time_thinking.destroy()
        #engine_opt.destroy()
        #engine_opt = None
    try:
        lvl = level.get()
        level.destroy()
    except:
        Btn3.destroy()
    select0()
    print(2)
    if mode =="bot" or mode == "play":
        w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
        w.create_text(320, 320, text="Don't forget to choose\nan opening book, if you want", font="Times 20", fill="green", tag="pieces")
        books = ["Nothing"]
        if "polyglot" in os.listdir():
            books += os.listdir("polyglot")
        variable.set("Nothing")
        opt = OptionMenu(tk, variable, *books)
        opt.pack()
    if mode != "analysis":
        Btn1 = Button(tk, text="White/player vs Black/AI", command=select4b)
        Btn1.pack()
        Btn2 = Button(tk, text="Black/player vs White/AI", command=select4w)
        Btn2.pack()


def select4w():
    """using AI -> ok -> bot or play -> white"""
    global player, book, opt, variable
    book = variable.get()
    opt.destroy()
    player="black"
    select5()


def select4b():
    """using AI -> ok -> bot or play -> black"""
    global player, book, opt, variable
    book = variable.get()
    opt.destroy()
    player="white"
    select5()


def select5():
    """using AI -> ok -> play or bot -> white or black"""
    global Engine, btn, opt, book, variable, WriteOption, write_opt, ok
    book = variable.get()
    opt.destroy()
    select0()
    if mode == "bot":
        WriteOption = StringVar()
        write_opt = Checkbutton(tk,
                            text="'write' option(write the move instead of using the mouse)",
                            variable=WriteOption,
                            onvalue="on",
                            offvalue="off")
        WriteOption.set("off")
        write_opt.pack()
        w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
        w.create_text(320, 320, text="Choose the website\n(make sure the chessboard is fully visible)\n\nTip: if you want to turn off the bot\nduring the game, put the\nmouse in the top-left corner", font="Times 20", fill="green", tag="pieces")
        websites = ["detect automatically(slower)"]
        if "images" in os.listdir():
            websites += os.listdir("images")
        variable.set("detect automatically(slower)")
        opt = OptionMenu(tk, variable, *websites)
        opt.pack()
        btn = Button(tk , text="ok", command=select6)
        btn.pack()
    else:
        w.create_text(320, 320, text="Double-Click anywhere to start", font="Times 20", fill="green", tag="pieces")
        Undo = Button(tk, text="undo", command=undo)
        Undo.pack()
        ok=True
        Btn = Button(tk, text="Back to the menu", command=main)
        Btn.pack()


def select6():
    """using AI -> ok -> bot -> white or black -> ok"""
    global btn, website, opt, player2, write_opt, write, ok
    write=WriteOption.get()=="on"#boolean
    w.itemconfigure("recognition", state="hidden")
    btn.destroy()
    write_opt.destroy()
    website = variable.get()
    opt.destroy()
    player2 = "white"  # player: user, player: AI/Bot
    if player == "white":
        player2 = "black"
    print(player2, website)
    ok=True
    Btn = Button(tk, text="Back to the menu", command=main)
    Btn.pack()
    bot()
    

def bot():
    """bot is coming..."""
    global website
    error =False
    if website=="detect automatically(slower)":
        websites=[]
        if "images" in os.listdir():
            websites += os.listdir("images")
        im = pyautogui.screenshot()
        for site in websites:
            with open("images/"+site+"/pixel.txt", "r") as f:
                f.readline()
                pixel2=eval(f.readline())
                f.close()
            try:
                for y in range(im.size[1]):
                    for x in range(im.size[0]):
                        rgb = im.getpixel((x, y))
                        if rgb in pixel2:
                            website=site
                            print(website)
                            raise TypeError
            except:
                error = True
    try:
        t=time.time()
        coord_board1=find_first_pixel(website)
        print(coord_board1)
        coord_board2 = find_last_pixel(website)
        print(coord_board2)
        print(time.time()-t)
        t=time.time()
        if error:
            raise TypeError
        
    except:  # if not found with image recognition, use the mouse to detect the corners
        nsec = 4
        pyautogui.alert(str(nsec)+"s for the mouse to be in the top left-hand corner of the board")
        sec = nsec
        Draw(player2)
        while sec>0:
            w.create_text(320, 320, text=str(sec)+"s for the mouse to be in the\ntop left-hand\ncorner of the board", fill="red", font="Times 20", tag="recognition")
            tk.update()
            sleep(1)
            sec-=1
            w.itemconfigure("recognition", state="hidden")
        coord_board1 = get_mouse_board()
        sec = nsec
        pyautogui.alert(str(nsec)+"s for the mouse to be in the lower right-hand corner of the board")
        while sec>0:
            w.create_text(320, 320, text=str(sec)+"s for the mouse to be in the\nlower right-hand\ncorner of the board", fill="red", font="Times 20", tag="recognition")
            tk.update()
            sleep(1)
            sec-=1
            w.itemconfigure("recognition", state="hidden")
        coord_board2 = get_mouse_board()
    coord_board = coord_board1+coord_board2
    if player2 == "white":
        if engine == "Krevetka":
            play_white(coord, lvl, book)
        else:
            play_engine(coord, engine, book, time2think, time_is_depth)
        Draw(player)
        if write:
            write_move(str(coord.move_stack[-1]))
        else:
            play_mouse(str(coord.move_stack[-1]), coord_board, player2=="black")
    while True:
        if coord.is_checkmate() or get_mouse_board() == [0, 0]:
            break
        if (coord.turn and player == "white") or (not coord.turn and player == "black"):  # player's turn
            move0 = get_move(coord_board1, coord_board2, player2, website)
            move1 = move0[0]+move0[1]  # e2e4 ?
            move2 = move0[1]+move0[0]  # or e4e2 ?
            l = list(map(str, coord.legal_moves))
            if (move1 in l) or (move1+"q" in l):
                move = move1
            elif (move2 in l) or (move2+"q" in l):
                move = move2
            elif "e1a1" in [move1, move2] and "e1c1" in l:
                move="e1c1"
            elif "e8a8" in [move1, move2] and "e8c8" in l:
                move="e8c8"
            elif "e1h1" in [move1, move2] and "e1g1" in l:
                move="e1g1"
            elif "e8h8" in [move1, move2] and "e8g8" in l:
                move="e8g8"
            else:
                move = "nothing"
            if move == "nothing":
                pass#-(sleep(time2think-0.1)
            else:
                play_human(move)
                play_human(move+"q")
                Draw(player2)
        else:  # bot's turn
            if engine == "Krevetka":
                if player2 == "white":
                    play_white(coord, lvl, book)
                else:
                    play_black(coord, lvl, book)
            else:
                play_engine(coord, engine, book, time2think, time_is_depth)
            if write:
                write_move(str(coord.move_stack[-1]))
                Draw(player2)
            else:
                play_mouse(str(coord.move_stack[-1]), coord_board, player2=="black")
                Draw(player2)


def undo():
    if coord.move_stack!=[]:
        coord.pop()
        if mode=="play" and coord.move_stack!=[]:
            coord.pop()
        Draw(player)


def analyse():
    board = coord.copy()
    play_engine(board, engine, "Nothing", time2think, time_is_depth)
    best = board.move_stack[-1]
    best = engine.play(coord, chess.engine.Limit(time2think)).move
    print(best)
    moves = analyse_position(coord, engine, time2think, time_is_depth)["moves"]
    if best not in moves:
        moves = [best]+moves
    best = str(best)
    w.itemconfigure("analyse", state="hidden")
    for Move in moves:
        if Move in coord.legal_moves:
            move = str(Move)
            x0 = "abcdefgh".find(move[0])*80+40
            x1 = "abcdefgh".find(move[2])*80+40
            y0 = 640-int(move[1])*80+40
            y1 = 640-int(move[3])*80+40
            color = ["blue", "red"][not coord.turn]
            if move == best:
                color = "green"
            w.create_line(x0, y0, x1, y1, fill=color, tag="analyse")
            board = coord.copy()
            board.push_san(move)
            try:
                #if time_is_depth:
                w.create_text(x1, y1, text=str(analyse_position(board, engine, time2think, time_is_depth)["score"].pov(True)), fill=color, font="Times 22", tag="analyse")
                #else:
                #    w.create_text(x1, y1, text=str(analyse_position(board, engine, 0.1, time_is_depth)["score"].pov(True)), fill=color, font="Times 22", tag="analyse")
            except:
                pass
            tk.update()


def click(event):
    """getting the position of the click and moving pieces"""
    global click_move, player, time_is_depth, time_thinking, last_choice
    print(time_is_depth)
    if engine_opt!=None:
        if EngineOption.get()!=last_choice:
            print(last_choice, EngineOption.get())
            last_choice=EngineOption.get()
            time_is_depth = EngineOption.get()=="off"
            tk.update()
            print(time_is_depth, EngineOption.get())
            time_thinking.destroy()
            if time_is_depth:
                time_thinking = Scale(tk, orient="horizontal", from_=1, to=50, resolution=1, tickinterval=5, length=500, label="depth")
                time_thinking.set(5)
                time_thinking.pack()
            else:
                time_thinking = Scale(tk, orient="horizontal", from_=0.1, to=10, resolution=0.1, tickinterval=1, length=400, label="time thinking")
                time_thinking.set(1)
                time_thinking.pack()
    elif mode != "start" and ok:
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
            if mode == "normal" or mode == "analysis":
                if coord.turn and mode == "normal":  #switching the point of view
                    player = "white"
                if not coord.turn and mode == "normal":
                    player = "black"
                if mode == "analysis":
                    pass
                    """
                    board = coord.copy()
                    play_engine(board, engine, "Nothing", time2think, time_is_depth)
                    best = board.move_stack[-1]
                    best = engine.play(coord, chess.engine.Limit(time2think)).move
                    print(best)
                    moves = analyse_position(coord, engine, time2think, time_is_depth)["moves"]
                    if best not in moves:
                        moves = [best]+moves
                    best = str(best)
                    w.itemconfigure("analyse", state="hidden")
                    for Move in moves:
                        if Move in coord.legal_moves:
                            move = str(Move)
                            x0 = "abcdefgh".find(move[0])*80+40
                            x1 = "abcdefgh".find(move[2])*80+40
                            y0 = 640-int(move[1])*80+40
                            y1 = 640-int(move[3])*80+40
                            color = ["blue", "red"][not coord.turn]
                            if move == best:
                                color = "green"
                            w.create_line(x0, y0, x1, y1, fill=color, tag="analyse")
                            board = coord.copy()
                            board.push_san(move)
                            try:
                                if time_is_depth:
                                    w.create_text(x1, y1, text=str(analyse_position(board, engine, time2think-1, time_is_depth)["score"].pov(True)), fill=color, font="Times 22", tag="analyse")
                            except:
                                pass
                            tk.update()
                        """
                else:
                    Draw(player)
            elif mode == "play":
                if player == "white" and not coord.turn:
                    if engine == "Krevetka":
                        play_black(coord, lvl, book)
                    else:
                        play_engine(coord, engine, book, time2think, time_is_depth)
                if player == "black" and coord.turn:
                    if engine == "Krevetka":
                        play_white(coord, lvl, book)
                    else:
                        play_engine(coord, engine, book, time2think, time_is_depth)
                verification(coord)
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


def main():
    global label, fen_starter, textFen, engine_opt, time_is_depth, ok, last_move, time2think, MusicOption, music_opt, Btn1, Btn2, tk, w, mode, click_move, player, engine, book, coord, last_choice
    while len(coord.move_stack)>0:
            coord.pop()
    try:
        tk.destroy()
        engine.quit()
    except:
        pass
    label = None #photo
    last_choice = "off"
    engine_opt = None #widget for engine option
    ok = False  # if we can activate the function Draw
    time2think = 1.0  # time thinking or depth, it depends of the boolean time_is_depth
    last_move = ""  # explicit
    time_is_depth = False  #the variable "time2think" is depth, not time
    mode = "start"  # start: nothing, normal: human vs human, play: AI vs human, bot: AI/you vs another person, analysis: explicit
    click_move = ""  # the squares where you click
    player = "white"
    engine = None  # 'None' in the normal mode
    book = "Nothing"  # name of the polyglot opening book choosen
    
    tk = Tk()
    tk.title("Chess")
    tk.resizable(False, False)
    tk.configure(cursor = "hand2")
    w = Canvas(tk,
               width=640,
               height=640,
               bg="#"+str(hex(238))[2:]+str(hex(216)[2:]+str(hex(181))[2:]))
    w.pack()
    for i in range(1, 9, 2):  # the squares of the board
        for j in range(1, 9, 2):
            w.create_rectangle(i*80,
                               (j-1)*80,
                               (i+1)*80,
                               j*80,
                               fill="#"+str(hex(181))[2:]+str(hex(136))[2:]+str(hex(99))[2:])
    
    for i in range(0, 9, 2):
        for j in range(0, 9, 2):
            w.create_rectangle(i*80,
                               (j-1)*80,
                               (i+1)*80,
                               j*80,
                               fill="#"+str(hex(181))[2:]+str(hex(136))[2:]+str(hex(99))[2:])
    w.create_rectangle(0, 0, 640, 640, fill="black", tag="pieces")
    MusicOption = StringVar()
    music_opt = Checkbutton(tk,
                            text="music option (tells the moves, and plays a song when it is the end of the game)",
                            variable=MusicOption,
                            onvalue="on",
                            offvalue="off")
    if "chess.gif" in os.listdir():
        photo = PhotoImage(file="chess.gif")
        label = Label(image=photo)
        label.place(x=0, y=0)
    else:
        w.create_text(320,
                      320,
                      text="''I don't Believe in psychology,\nI believe in good moves''\nBobby Fischer\n"+chr(9818)+chr(9819)+chr(9820)+chr(9821)+chr(9822)+chr(9823),
                      font="Times 20",
                      fill="red",
                      tag="pieces")
    MusicOption.set("off")
    music_opt.pack()
    textFen = Entry(tk, width=50)
    textFen.insert(0, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    textFen.pack()
    Btn1 = Button(tk, text="human vs human", overrelief="ridge", command=select1)
    Btn1.pack()
    Btn2 = Button(tk, text="against AI", overrelief="ridge", command=select2)
    Btn2.pack()
    w.bind_all("<Button-1>", click)
    tk.mainloop()


if __name__ == "__main__":
    main()
