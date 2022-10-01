import chess
import chess.polyglot
import chess.engine
import chess.syzygy
import copy
import time
from random import *
import os
from tools import *
win = True
try:
    from winsound import Beep
except:
    win = False

coord = chess.Board()#"2k5/8/8/8/8/3R4/3K4/8")


def new_board():
    global coord
    coord = chess.Board()

    
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
    
    c = string_coord(board)
    score = 0
    val = {" ": 0, ".": 0, "p": -100, "P": 100, "n": -320, "N": 320, "b": -330,
           "B": 330, "q": -880, "Q": 880, "r": -510, "R": 510, "k": 0, "K": 0}
    for i in c:
        score += val[i]  # material difference
    for i in range(64):
        if board.is_attacked_by(chess.WHITE, i):  # possible moves
            if i in [27, 28, 35, 36]:  # in the center by white
                score += 20
            else:
                score += 10
        if board.is_attacked_by(chess.BLACK, i):
            if i in [27, 28, 35, 36]:  # in the center by black
                score -= 20
            else:
                score -= 10
    #score += c[8:16].count("P")*100 #pion passé 7e rangée
    #score -= c[48:56].count("p")*100
    #score += c[16:24].count("P")*80 #pion 6e rangée
    #score -= c[40:48].count("p")*80
    #score += c[:8].count("n")*5
    #score -= c[56:].count("N")*5
    #score += board.is_attacked_by(chess.WHITE, 27)+board.is_attacked_by(chess.WHITE, 28)+board.is_attacked_by(chess.WHITE, 35)+board.is_attacked_by(chess.WHITE, 36)
    #score -= board.is_attacked_by(chess.BLACK, 27)+board.is_attacked_by(chess.BLACK, 28)+board.is_attacked_by(chess.BLACK, 35)+board.is_attacked_by(chess.BLACK, 36)
    if "R" in c[8:16]:
        score += 200  # tour en 7e rangée
    if "r" in c[48:56]:
        score -= 200
    if board.is_stalemate() or coord.can_claim_draw():
        score = 0
    elif board.is_checkmate():
        score = 10000
        if board.turn:
            score *= -1
    return score


def use_syzygy():
    try:
        if len(list(coord.legal_moves))>0:#"syzygy/3-4-5" in os.listdir() and len(coord.piece_map())<=5:
            with chess.syzygy.open_tablebase("syzygy/3-4-5") as tablebase:
                eval_pos = tablebase.get_dtz(coord)
                if eval_pos != None:
                    print("table",tablebase.get_dtz(coord))
                    print("moves",len(list(coord.legal_moves)))
                    for move in list(coord.legal_moves):
                        #print(move)
                        board=coord.copy()
                        board.push_san(str(move))
                        if board.is_checkmate():
                            return str(move)
                        print(str(move),tablebase.get_dtz(board))
                        eval_move=tablebase.get_dtz(board)
                        if eval_pos==-eval_move+1 and eval_move!=0:
                            return str(move)
                else:
                    return ""
        return ""
    except Exception as e:
        print(e)
        return ""


def analyse_position(board, engine, time_thinking=1, time_is_depth=False):
    """TODO"""
    if time_is_depth:
        analysis = engine.analyse(board, chess.engine.Limit(depth=time_thinking))
    else:
        analysis = engine.analyse(board, chess.engine.Limit(time=time_thinking))
    return {"score": analysis["score"],
            "moves": analysis["pv"],
            "depth": analysis["depth"]}


def play_engine(board, engine, book="Nothing", time_thinking=1, time_is_depth=False):
    """using other chess engines"""
    move = play_auto(board, book)
    if move != None:
        board.push_san(move)
    else:
        if time_is_depth:
            result = engine.play(board, chess.engine.Limit(depth=time_thinking))
        else:
            result = engine.play(board, chess.engine.Limit(time=time_thinking))
        board.push(result.move)
        draw()


def play_auto(board, book="Nothing"):
    """playing automatically some moves"""
    opening_moves = []
    move = None
    print(book)
    if "polyglot" in os.listdir():
        if book in os.listdir("polyglot"):
            with chess.polyglot.open_reader("polyglot/"+book) as reader:
                for entry in reader.find_all(board):
                    opening_moves.append(entry.move)
    possible_move = ""
    if len(list(board.legal_moves)) == 1:
        move = str(list(board.legal_moves)[0])
    elif 1==1:  # end of game already known
        possible_move = use_syzygy()
    if len(opening_moves)>0:
        move = str(choice(opening_moves))
    elif possible_move!="":
        move = str(possible_move)
    return move


def play_random(board, book="baron30.bin"):
    """playing random moves"""
    n = play_auto(board, book)
    if n is None:
        n = str(choice(list(board.legal_moves)))
    board.push_san(str(n))


def play_black3(board, book="baron30.bin", evaluation=evaluate):
    t = time.time()
    opening_moves = []
    move = play_auto(board, book)
    if move is None:
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
    board.push_san(str(move))
    if win:
        Beep(400, 100)
    print(str(board.move_stack[-1]))
    print("time:",time.time() - t,"sec")
    print("evaluation:",evaluation(board))


def play_white3(board, book="baron30.bin", evaluation=evaluate):
    t = time.time()
    move = play_auto(board, book)
    if move is None:
        l = list(map(str,board.legal_moves))
        n={}
        for i in l:
            coord2=copy.copy(board)
            coord2.push_san(i)
            N = {}
            l2 = list(map(str,coord2.legal_moves))
            if l2 == []:
                e2=evaluation(coord2)
                n[e2] = i
                if evaluate(coord2) == 1000:move = i;break
            else:
                for j in l2:
                    coord3=copy.copy(coord2)
                    coord3.push_san(j)
                    M = {}
                    l3 = list(map(str,coord3.legal_moves))
                    if l3 == []:
                        N[evaluation(coord3)] = j
                    else:
                        for k in l3:
                            coord4=copy.copy(coord3)
                            coord4.push_san(k)
                            e4 = evaluation(coord4)
                            M[e4] = k
                            if evaluate(coord4) == 1000:
                                break
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


def play_white2(board, book="baron30.bin", evaluation=evaluate):
    t = time.time()
    move = play_auto(board, book)
    if move is None:
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


def play_black2(board, book="baron30.bin", evaluation=evaluate):
    t = time.time()
    move = play_auto(board, book)
    if move is None:
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

def play_white1(board, book="baron30.bin", evaluation=evaluate):
    t = time.time()
    move = play_auto(board, book)
    if move is None:
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


def play_black1(board, book="Nothing", evaluation=evaluate):
    t = time.time()
    move = play_auto(board, book)
    if move is None:
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


def play_white(board, lvl, book):
    if lvl == 0:
        play_random(board, book)
    elif lvl == 1:
        play_white1(board, book)
    elif lvl == 2:
        play_white2(board, book)
    else:
        play_white3(board, book)


def play_black(board, lvl, book):
    if lvl == 0:
        play_random(board, book)
    elif lvl == 1:
        play_black1(board, book)
    elif lvl == 2:
        play_black2(board, book)
    else:
        play_black3(board, book)


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

