import chess
import copy
import time
from random import *
win = True
try:
    from winsound import Beep
except:
    win = False
coord = chess.Board()
turn = 0
TURN = 0
list_moves=[]
book = {}
with open("chess_opening.txt","r") as f:
    val = f.read()
    if val=="":
        val="{}"
    exec("book="+val)
    f.close()

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


def play_random(board):
    global turn
    turn = abs(turn - 1)
    n = str(choice(list(board.legal_moves)))
    board.push_san(n)


def play_black2(board):
    global turn, list_moves, TURN
    betascore = 100
    t=time.time()
    TURN += 0.5
    turn = 1
    if string_coord(coord) in book:
        move = book[string_coord(coord)]
    else:
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
                            if evaluation(coord4) > betascore:
                                break
                        N[min(M)]=j
                        betascore = max(N)
                n[max(N)]=i
            move = n[min(n)]
    turn = 1
    board.push_san(move)
    list_moves.append(move)
    print(time.time() - t)


def play_black(board):
    global turn, list_moves, book, TURN
    t=time.time()
    TURN += 0.5
    turn = 1
    actual_coord = evaluation(coord)
    if string_coord(coord) in book:
        move = book[string_coord(coord)]
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
                if e2 == -100:move = i;break
            else:
                for j in l2:
                    turn = 0
                    coord3=copy.copy(coord2)
                    coord3.push_san(j)
                    M={}
                    l3=list(map(str,coord3.legal_moves))
                    if l3 == []:
                        N[evaluation(coord3)] = j
                    else:
                        for k in l3:
                            turn = 1
                            coord4=copy.copy(coord3)
                            coord4.push_san(k)
                            e4=evaluation(coord4)
                            M[e4] = k
                            if e4 == -100:break
                        N[min(M)]=j
                n[max(N)]=i
            move = n[min(n)]
            book = book | {string_coord(coord):move}
            if TURN <= 10.0:
                with open("chess_opening.txt","w")as f:
                    f.write(str(book))
                    f.close()               
    turn = 1
    board.push_san(move)
    list_moves.append(move)
    if win:
        Beep(400, 100)
    print(time.time() - t)


def play_white(board):
    global turn, list_moves, book, TURN
    t=time.time()
    TURN += 0.5
    turn = 0
    actual_coord = evaluation(coord)
    if string_coord(coord) in book:move = book[string_coord(coord)]
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
                if e2 == 100:move = i;break
            else:
                for j in l2:
                    turn = 1
                    coord3=copy.copy(coord2)
                    coord3.push_san(j)
                    M={}
                    l3=list(map(str,coord3.legal_moves))
                    if l3 == []:
                        N[evaluation(coord3)] = j
                    else:
                        for k in l3:
                            turn = 0
                            coord4=copy.copy(coord3)
                            coord4.push_san(k)
                            e4=evaluation(coord4)
                            M[e4] = k
                            if e4 == 100:break
                        N[max(M)]=j
                n[min(N)]=i
            move = n[max(n)]
            book = book | {string_coord(coord):move}
            if TURN <= 10.0:
                with open("chess_opening.txt","w")as f:
                    f.write(str(book))
                    f.close()
    turn = 0
    board.push_san(move)
    list_moves.append(move)
    if win:
        Beep(400, 100)
    print(time.time() - t)

def play_human(move, mode="normal"):
    global turn, list_moves, book
    turn = abs(turn-1)
    if move in list(map(str,coord.legal_moves)):
        list_moves.append(move)
        if mode=="learn":
            book = book | {string_coord(coord):move}
            with open("chess_opening.txt","w")as f:
                f.write(str(book))
                f.close()
        coord.push_san(move)
    
def evaluation(board):
    c=string_coord(board)
    score = 0
    val = {" ":0, ".":0,"p":-1,"P":1,"n":-3.2,"N":3.2,"b":-3.33,"B":3.33,"q":-8.8,"Q":8.8,"r":-5.1,"R":5.1,"k":-100,"K":100}
    for i in c:score+=val[i]
    if board.is_check():
        if turn == 0:score+=0.1
        else:score-=0.1
    if "k" in [c[2], c[16]] and not coord.has_castling_rights("black"):score -= 0.1
    if "K" in [c[~2+1], c[~16+1]] and not coord.has_castling_rights("white"):score += 0.1
    if board.is_stalemate() or coord.can_claim_draw():score = 0
    elif board.is_checkmate():
        score = 100
        if turn == 1:score *= -1
    return score

def mc_evaluation(board):
    global turn
    c=string_coord(board)
    score = 0
    if board.is_stalemate() or board.can_claim_draw():
        return  0
    elif board.is_checkmate():
        score = 100
        if turn == 1:
            score *= -1
        return score
    else:
        coordeval = copy.copy(board)
        Turn = turn
        for j in range(20):
            for i in range(200):
                try:
                    play_random(coordeval)
                except:
                    if coordeval.is_stalemate() or coordeval.can_claim_draw():
                        score+=0
                    elif coordeval.is_checkmate():
                        score += 1
                        if turn == 1:
                            score -= 2
                    break
            if i==199:
                score+=evaluation(board)/10
        turn = Turn
    return score

if __name__ == "__main__":
    while True not in [coord.is_checkmate(), coord.is_stalemate()]:
        draw()
        #play_white(coord)
        play_human(input("move:"))
        draw()
        if True not in [coord.is_checkmate(), coord.is_stalemate()]:
            play_black(coord)
            #play_human(input("move"))
        elif coord.is_stalemate():
            print("DRAW")
        else:
            print("Checkmate")
    if coord.is_stalemate():
        print("DRAW")
    else:
        print("Checkmate")
