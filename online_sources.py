from urllib.request import urlopen
from time import time

def lichess_board(url):
    t = time()
    data = str(urlopen(url).read())
    data = data[data.find("1. "):data.find("""*</div></div></aside><div class="round__board main-board">""")].split()
    real_data = []
    for moves in data:
        if not "." in moves:
            real_data.append(moves)
    print(time()-t)
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
        print(time()-t)
    except:
        data = ""
    return data
