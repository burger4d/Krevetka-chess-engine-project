# Krevetka-chess-engine-project

![screen_chess](https://user-images.githubusercontent.com/104983707/215318392-d886b374-1d63-421b-96d2-87f949163c7e.PNG)

![chess](https://user-images.githubusercontent.com/104983707/175565331-460224df-c0cf-4618-8e6c-e00ce4897f14.PNG)

A basic chess engine coded in python, with a GUI that allows you to use other stronger chess engines as Bots.


# Why Krevetka?
The name "Krevetka" means 🍤"shrimp"🦐.
It is in the same spirit like other chess engines, for example Rybka or stockfish (note that "Rybka" means "fish"🐟)

# The algorithm:
Wikipedia's definition: Minimax is a decision rule used in artificial intelligence, decision theory, game theory, statistics, and philosophy for minimizing the possible loss for a worst case (maximum loss) scenario. When dealing with gains, it is referred to as "maximin"—to maximize the minimum gain. Originally formulated for n-player zero-sum game theory, covering both the cases where players take alternate moves and those where they make simultaneous moves, it has also been extended to more complex games and to general decision-making in the presence of uncertainty.

Krevetka uses this algorithm, with a depth of 3. I didn't do the algorithm in its recursive version, but only with some "for" loops(faster).
# Folders:
-engines:
The other chess engines that you can use(you must put ONLY the executable files). Actually, there is only the free version of Komodo(here: https://komodochess.com/downloads.htm). For sure, you can also add other chess engines, like Stockfish on https://stockfishchess.org/download/(I didn't add it because the file was larger than 25MB).

-images:
The rgb values of the "yellow" squares on each website.

-polyglot:
The different polyglot chess opening books found here: https://chess.stackexchange.com/questions/35448/looking-for-polyglot-opening-books?adlt=strict&toWww=1&redig=95BF7929665C40C0966EB2870AA78E90

# Files:
-krevetka.py:
The code of the chess engine.

-main.py:
The file with the GUI.

-endgame.mp3:
Actually, this is the song "hard as steel" from abbynoise, a Non Copyright Song(NCS). You can play it when the game is finished.

-tools.py:
This file is a homemade API. The AI can have access to the endgame tablebase syzygy (here👉https://syzygy-tables.info/?adlt=strict&toWww=1&redig=7B4251AD8D5542B89B81810568F3680B), and can also play game against someone on lichess, just by giving the position of the other board on the screen (I didn't use the LichessAPI, due to the procrastinization when I must read its documentation and also because I wanted to improve my skills in python, with pyautogui).

-README.md:
The file that you are currently reading.

# Lichess account:
⚠WARNING⚠: NOTE THAT ANYONE USING THIS BOT FOR CHEATING WILL BE BANNED(quiet logic I think). EVEN THOUGH YOU ARE USING IT WITH A LICHESS BOT ACCOUNT, YOU MUST KNOW THAT THIS BOT DOES NOT USE THE LICHESS API, AND FOR THAT REASON THIS BOT WILL BREAK THE TERMS OF SERVICE OF LICHESS.
(note that I am working on the implementation of the lichess API, so be patient)
PS: note also that using bots on online chess platforms is considered as cheating.

here: 👉https://lichess.org/@/KrevetkaBot
![game](https://user-images.githubusercontent.com/104983707/170866422-873fb47d-0310-46db-b7e9-55fbe7cb5910.gif)

# Run it!
run this command in the cmd: pip install -r requirements.txt

You must run the main.py file, if you want to play with the GUI(You can play without AI in the command just by running the krevetka.py file). I will also recommend to run it with the python interpreter pypy(here 👉 https://www.pypy.org/), dividing by two the waiting time(maximum 60s without, vs 30s with)).


(PS: There is a lot of code that is redundant and there are tons of improvements that can be made.)
