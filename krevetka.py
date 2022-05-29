import chess
import chess.polyglot
import copy
import time
from random import *
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
    print(evaluation(coord))  # mc_evaluation(coord))


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

def play_black(board):
    t = time.time()
    actual_coord = evaluation(coord)
    with chess.polyglot.open_reader("baron30.bin") as reader:
        opening_moves = []
        for entry in reader.find_all(coord):
            opening_moves.append(entry.move)
    """
    if string_coord(coord) in book:
        move = book[string_coord(coord)]
    """
    possible_move = ""
    if len(board.move_stack) == 1:
        move = str(board.move_stack)
    elif use_syzygy():
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
                if e2 == -1000:move = i;break
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
                            if e4 == -1000:break
                        N[min(M)]=j
                n[max(N)]=i
            move = n[min(n)]
            """
            book = book | {string_coord(coord):move}
            if TURN <= 5:
                with open("chess_opening.txt","w")as f:
                    f.write(str(book))
                    f.close()
            """
    board.push_san(move)
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time:",time.time() - t,"sec")
    print("evaluation:",evaluation(board))


def play_white(board):
    t = time.time()
    actual_coord = evaluation(coord)
    with chess.polyglot.open_reader("baron30.bin") as reader:
        opening_moves = []
        for entry in reader.find_all(coord):
            opening_moves.append(entry.move)
    """
    if string_coord(coord) in book:
        move = book[string_coord(coord)]
    """
    possible_move = ""
    if len(board.move_stack) == 1:
        move = str(board.move_stack)
    elif use_syzygy():
        possible_move = syzygy(board.fen())
    if len(opening_moves)>0:
        move = str(choice(opening_moves))
    elif possible_move!="":
        move = possible_move
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
                if e2 == 1000:move = i;break
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
                            if e4 == 1000:break
                        N[max(M)]=j
                n[min(N)]=i
            move = n[max(n)]
            """
            book = book | {string_coord(coord):move}
            if TURN <= 5:
                with open("chess_opening.txt","w")as f:
                    f.write(str(book))
                    f.close()
            """
    board.push_san(move)
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time",time.time() - t,"sec")
    print("evaluation:",evaluation(board))
'''
def white():
    pass

def black(coord):
    liste = list(map(str,coord.legal_moves))
    values = {}
    for move in liste:
        child = copy.copy(coord)
        child.push_san(move)
        EVAL_CHILD = minimax(child, 2, False)
        values[EVAL_CHILD] = move
    pprint(values)
    move = values[min(values)]
    print(move)
    coord.push_san(move)
'''
def play_human(move):
    try:
        coord.push_san(move)
        print(str(coord.move_stack[-1]))
        print("evaluation:", evaluation(coord))
        print(move)
    except ValueError:
        pass
    
def evaluation(board):
    c=string_coord(board)
    score = 0
    val = {" ":0, ".":0,"p":-10,"P":10,"n":-32,"N":32,"b":-33,"B":33,"q":-88,"Q":88,"r":-51,"R":51,"k":-1000,"K":1000}
    for i in c:
        score += val[i]#difference de materiel
    for i in range(64):
        if board.is_attacked_by(chess.WHITE, i):#liberté de mouvements
            score += 1
        if board.is_attacked_by(chess.BLACK, i):
            score -= 1
    score += c[8:16].count("P")*20 #pion passé
    score -= c[48:56].count("p")*20
    score += c[16:24].count("P")*15 #pion passé
    score -= c[40:48].count("p")*15
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


if __name__ == "__main__":
    while True not in [coord.is_checkmate(), coord.is_stalemate()]:
        draw()
        #play_white(coord)
        play_human(input("move:"))
        draw()
        if True not in [coord.is_checkmate(), coord.is_stalemate()]:
            #play_black(coord)
            #black()
            play_human(input("move"))
        elif coord.is_stalemate():
            print("DRAW")
        else:
            print("Checkmate")
    if coord.is_stalemate():
        print("DRAW")
    else:
        print("Checkmate")
