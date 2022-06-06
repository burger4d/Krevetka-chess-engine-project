import chess
import chess.polyglot
import copy
import time
from random import *
import os
from online_sources import syzygy
win = True
try:
    from winsound import Beep
except:
    win = False
coord = chess.Board()
    
"""
book = {}
try:

    with open("chess_opening.txt","r") as f:
        val = f.read()
        if val=="":
            val="{}"
        exec("book="+val)
        f.close()
except:
    pass
"""
def draw():
    print("a b c d e f g h\n---------------")
    print(coord)
    print(evaluate(coord))  # mc_evaluation(coord))


def string_coord(board):
    c=""
    for i in str(board):
        if i!="\n":
            if i!=" ":
                c+=i
    return c
"""
def minimax(node, depth, maxplayer):
    EVAL = evaluation(node)
    if depth == 0 or EVAL in [0, -100, 100]:
        return EVAL
    if maxplayer:#blancs=True, nors=False
        value = -100
        for move in list(map(str,node.legal_moves)):
            child = copy.copy(node)
            child.push_san(move)
            value = max(value, minimax(child, depth - 1, False))
    else:
        value = 100
        for move in list(map(str,node.legal_moves)):
            child = copy.copy(node)
            child.push_san(move)
            value = min(value, minimax(child, depth - 1, True))
    return value
"""
def evaluate(board):
    c=string_coord(board)
    score = 0
    val = {" ":0, ".":0,"p":-10,"P":10,"n":-32,"N":32,"b":-33,"B":33,"q":-88,"Q":88,"r":-51,"R":51,"k":-1000,"K":1000}
    for i in c:
        score += val[i]#difference de materiel
    for i in range(64):
        if board.is_attacked_by(chess.WHITE, i):#liberté de mouvements
            if i in [27,28,35,36]:
                score += 2
            else:
                score += 1
        if board.is_attacked_by(chess.BLACK, i):
            if i in [27,28,35,36]:
                score -= 2
            else:
                score -= 1
    score += c[8:16].count("P")*10 #pion passé 7e rangée
    score -= c[48:56].count("p")*10
    score += c[16:24].count("P")*8 #pion 6e rangée
    score -= c[40:48].count("p")*8
    #score += c[:8].count("n")*5
    #score -= c[56:].count("N")*5
    #score += board.is_attacked_by(chess.WHITE, 27)+board.is_attacked_by(chess.WHITE, 28)+board.is_attacked_by(chess.WHITE, 35)+board.is_attacked_by(chess.WHITE, 36)
    #score -= board.is_attacked_by(chess.BLACK, 27)+board.is_attacked_by(chess.BLACK, 28)+board.is_attacked_by(chess.BLACK, 35)+board.is_attacked_by(chess.BLACK, 36)
    if "R" in c[8:16]:
        score+=20#tour en 7e rangée
    if "r" in c[48:56]:
        score-=20
    if board.is_stalemate() or coord.can_claim_draw():
        score = 0
    elif board.is_checkmate():
        score = 1000
        if board.turn:
            score *= -1
    return score

def use_syzygy():
    return len(coord.piece_map())<=10

def play_random(board):
    n = str(choice(list(board.legal_moves)))
    board.push_san(n)

'''
def play_black2(board):
    global turn, list_moves, TURN
    t=time.time()
    TURN += 0.5
    turn = 1
    """
    if string_coord(coord) in book:
        move = book[string_coord(coord)]
    else:
    """
    if True:
        l=list(map(str,board.legal_moves))
        n={}
        for i in l:
            coord2=copy.copy(board)
            coord2.push_san(i)
            N={}
            if list(map(str,coord2.legal_moves)) == []:
                n[evaluation(coord2)] = i
            else:
                for j in list(map(str,coord2.legal_moves)):
                    turn = 0
                    coord3=copy.copy(coord2)
                    coord3.push_san(j)
                    M={}
                    if list(map(str,coord3.legal_moves)) == []:
                        N[evaluation(coord3)] = j
                    else:
                        for k in list(map(str,coord3.legal_moves)):
                            turn = 1
                            coord4=copy.copy(coord3)
                            coord4.push_san(k)
                            M[evaluation(coord4)] = k
                        N[min(M)]=j
                        
                n[max(N)]=i
            move = n[min(n)]
    turn = 1
    board.push_san(move)
    list_moves.append(move)
    print(time.time() - t)
'''

def play_black3(board, evaluation=evaluate):
    t = time.time()
    actual_coord = evaluation(coord)
    opening_moves = []
    if "baron30.bin" in os.listdir():
        with chess.polyglot.open_reader("baron30.bin") as reader:
            for entry in reader.find_all(coord):
                opening_moves.append(entry.move)
    possible_move = ""
    if len(board.move_stack) == 1:
        move = str(board.move_stack)
    elif use_syzygy():#fin de partie deja connue
        possible_move = syzygy(board.fen())
    if len(opening_moves)>0:
        move = str(choice(opening_moves))
    elif possible_move!="":
        move = possible_move
    else:
        l = list(map(str, board.legal_moves))
        n = {}
        for i in l:
            coord2=copy.copy(board)
            coord2.push_san(i)
            N = {}
            l2=list(map(str,coord2.legal_moves))
            if l2 == []:
                e2=evaluation(coord2)
                n[e2] = i
                if evaluate(coord2) == -1000:move = i;break
            else:
                for j in l2:
                    coord3=copy.copy(coord2)
                    coord3.push_san(j)
                    M={}
                    l3=list(map(str,coord3.legal_moves))
                    if l3 == []:
                        N[evaluation(coord3)] = j
                    else:
                        for k in l3:
                            coord4=copy.copy(coord3)
                            coord4.push_san(k)
                            e4=evaluation(coord4)
                            M[e4] = k
                            if evaluate(coord4) == -1000:break
                        N[min(M)]=j
                n[max(N)]=i
            move = n[min(n)]
    board.push_san(move)
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time:",time.time() - t,"sec")
    print("evaluation:",evaluation(board))


def play_white3(board, evaluation=evaluate):
    t = time.time()
    actual_coord = evaluation(coord)
    opening_moves = []
    if "baron30.bin" in os.listdir():
        with chess.polyglot.open_reader("baron30.bin") as reader:
            for entry in reader.find_all(coord):
                opening_moves.append(entry.move)
    move = ""
    possible_move = ""
    possible_move2 = find_pgn(board.fen())
    if len(board.move_stack) == 1:
        move = str(board.move_stack)
    elif use_syzygy():
        possible_move = syzygy(board.fen())
    if len(opening_moves)>0:
        move = str(choice(opening_moves))
    elif possible_move!="":
        move = possible_move
    elif possible_move2!=None:
        move = possible_move2
    else:
        l=list(map(str,board.legal_moves))
        n={}
        for i in l:
            coord2=copy.copy(board)
            coord2.push_san(i)
            N={}
            l2=list(map(str,coord2.legal_moves))
            if l2 == []:
                e2=evaluation(coord2)
                n[e2] = i
                if evaluate(coord2) == 1000:move = i;break
            else:
                for j in l2:
                    coord3=copy.copy(coord2)
                    coord3.push_san(j)
                    M={}
                    l3=list(map(str,coord3.legal_moves))
                    if l3 == []:
                        N[evaluation(coord3)] = j
                    else:
                        for k in l3:
                            coord4=copy.copy(coord3)
                            coord4.push_san(k)
                            e4=evaluation(coord4)
                            M[e4] = k
                            if evaluate(coord4) == 1000:break
                        N[max(M)]=j
                n[min(N)]=i
            move = n[max(n)]
    board.push_san(move)
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time",time.time() - t,"sec")
    print("evaluation:",evaluation(board))

def play_human(move):
    try:
        coord.push_san(move)
        print(str(coord.move_stack[-1]))
        print("evaluation:", evaluate(coord))
        print(move)
    except ValueError:
        pass

def deep_eval(board, depth=3, number=100):
    score = 0
    for i in range(number):
        child = copy.copy(board)
        for j in range(depth):
            try:
                play_random(child)
            except IndexError:
                break
        score += evaluate(child)
    return score

def play_white2(board, evaluation=evaluate):
    t = time.time()
    actual_coord = evaluation(coord)
    opening_moves = []
    if "baron30.bin" in os.listdir():
        with chess.polyglot.open_reader("baron30.bin") as reader:
            for entry in reader.find_all(coord):
                opening_moves.append(entry.move)
    move = ""
    possible_move = ""
    possible_move2 = find_pgn(board.fen())
    if len(board.move_stack) == 1:
        move = str(board.move_stack)
    elif use_syzygy():
        possible_move = syzygy(board.fen())
    if len(opening_moves)>0:
        move = str(choice(opening_moves))
    elif possible_move!="":
        move = possible_move
    elif possible_move2!=None:
        move = possible_move2
    else:
        l=list(map(str,board.legal_moves))
        n={}
        for i in l:
            coord2=copy.copy(board)
            coord2.push_san(i)
            N={}
            l2=list(map(str,coord2.legal_moves))
            if l2 == []:
                e2=evaluation(coord2)
                n[e2] = i
                if evaluate(coord2) == 1000:
                    move = i
                    break
            else:
                for j in l2:
                    coord3=copy.copy(coord2)
                    coord3.push_san(j)
                    N[evaluation(coord3)] = j
                n[min(N)]=i
            move = n[max(n)]
    board.push_san(move)
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time",time.time() - t,"sec")
    print("evaluation:",evaluation(board))

def play_black2(board, evaluation=evaluate):
    t = time.time()
    actual_coord = evaluation(coord)
    opening_moves = []
    if "baron30.bin" in os.listdir():
        with chess.polyglot.open_reader("baron30.bin") as reader:
            for entry in reader.find_all(coord):
                opening_moves.append(entry.move)
    possible_move = ""
    if len(board.move_stack) == 1:
        move = str(board.move_stack)
    elif use_syzygy():#fin de partie deja connue
        possible_move = syzygy(board.fen())
    if len(opening_moves)>0:
        move = str(choice(opening_moves))
    elif possible_move!="":
        move = possible_move
    else:
        l = list(map(str, board.legal_moves))
        n = {}
        for i in l:
            coord2=copy.copy(board)
            coord2.push_san(i)
            N = {}
            l2=list(map(str,coord2.legal_moves))
            if l2 == []:
                e2=evaluation(coord2)
                n[e2] = i
                if evaluate(coord2) == -1000:
                    move = i
                    break
            else:
                for j in l2:
                    coord3=copy.copy(coord2)
                    coord3.push_san(j)
                    N[evaluation(coord3)] = j
                n[max(N)]=i
            move = n[min(n)]
    board.push_san(move)
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time:",time.time() - t,"sec")
    print("evaluation:",evaluation(board))

def play_white1(board, evaluation=evaluate):
    t = time.time()
    actual_coord = evaluate(coord)
    opening_moves = []
    if "baron30.bin" in os.listdir():
        with chess.polyglot.open_reader("baron30.bin") as reader:
            for entry in reader.find_all(coord):
                opening_moves.append(entry.move)
    move = ""
    possible_move = ""
    possible_move2 = find_pgn(board.fen())
    if len(board.move_stack) == 1:
        move = str(board.move_stack)
    elif use_syzygy():
        possible_move = syzygy(board.fen())
    if len(opening_moves)>0:
        move = str(choice(opening_moves))
    elif possible_move!="":
        move = possible_move
    elif possible_move2!=None:
        move = possible_move2
    else:
        l=list(map(str,board.legal_moves))
        n={}
        for i in l:
            coord2 = copy.copy(board)
            coord2.push_san(i)
            n[evaluation(coord2)] = i
            move = n[max(n)]
    board.push_san(move)
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time",time.time() - t,"sec")
    print("evaluation:",evaluation(board))

def play_black1(board, evaluation=evaluate):
    t = time.time()
    actual_coord = evaluate(coord)
    opening_moves = []
    if "baron30.bin" in os.listdir():
        with chess.polyglot.open_reader("baron30.bin") as reader:
            for entry in reader.find_all(coord):
                opening_moves.append(entry.move)
    move = ""
    possible_move = ""
    possible_move2 = find_pgn(board.fen())
    if len(board.move_stack) == 1:
        move = str(board.move_stack)
    elif use_syzygy():
        possible_move = syzygy(board.fen())
    if len(opening_moves)>0:
        move = str(choice(opening_moves))
    elif possible_move!="":
        move = possible_move
    elif possible_move2!=None:
        move = possible_move2
    else:
        l=list(map(str,board.legal_moves))
        n={}
        for i in l:
            coord2 = copy.copy(board)
            coord2.push_san(i)
            n[evaluation(coord2)] = i
        move = n[min(n)]
    board.push_san(move)
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time",time.time() - t,"sec")
    print("evaluation:",evaluation(board))

def play_white(board, lvl=3):
    if lvl == 0:
        play_random(board)
    elif lvl == 1:
        play_white1(board)
    elif lvl == 2:
        play_white2(board)
    else:
        play_white3(board)

def play_black(board, lvl=3):
    if lvl == 0:
        play_random(board)
    elif lvl == 1:
        play_black1(board)
    elif lvl == 2:
        play_black2(board)
    else:
        play_black3(board)
    
if __name__ == "__main__":
    while True not in [coord.is_checkmate(), coord.is_stalemate()]:
        draw()
        #play_white(coord)
        play_human(input("move:"))
        draw()
        if True not in [coord.is_checkmate(), coord.is_stalemate()]:
            #play_black(coord)
            #black()
            play_human(input("move:"))
        elif coord.is_stalemate():
            print("DRAW")
        else:
            print("Checkmate")
    if coord.is_stalemate():
        print("DRAW")
    else:
        print("Checkmate")
