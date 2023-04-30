# Krevetka-chess-engine-project

![screen_chess](https://user-images.githubusercontent.com/104983707/215318392-d886b374-1d63-421b-96d2-87f949163c7e.PNG)

![chess](https://user-images.githubusercontent.com/104983707/175565331-460224df-c0cf-4618-8e6c-e00ce4897f14.PNG)

A basic chess engine coded in python, with a GUI that enables you to utilize more advanced chess engines as bots.


# Why Krevetka?
The name "Krevetka" means 🍤"shrimp"🦐 in russian. The use of a marine animal is in the spirit of great engines such as Stockfish, or Rybka.

# The "image recognition"
The software captures a screenshot and searches each individual pixel for colors belonging to the chessboard. It then determines the chessboard's location on the screen, ensuring its complete visibility, and begins playing. The program continually scans for any color modifications on two squares, indicating a piece has been moved, and deduces the last move made. While you can change pieces, the program requires the colors to remain the same, and moving the chessboard or altering its size during the game is forbidden.

Currently, the software is compatible with the following websites: 
- lichess
- chess.com
- chessfriends
- chess24

# The Algorithm:
The minimax algorithm explores every possible position up to a predetermined depth. It executes a recursive function which evaluates each position and determines the optimal move. Krevetka uses this algorithm with a maximum depth of three. Instead of a recursive function, I implemented it using "for" loops, as these tend to be quicker in Python.

# Folders:
- engines: Other chess engines which can be used (Please only include the executable files). You may find some useful engines here: https://chess-bot.com/blog/chess-engines-download.html
- images: The RGB values of the highlighted squares on each websites. For illustration, if you play e2e4, both e2 and e4 will be illuminated.
- polyglot: Various polyglot chess opening books available for selection here: https://chess.stackexchange.com/questions/35448/looking-for-polyglot-opening-books?adlt=strict&toWww=1&redig=95BF7929665C40C0966EB2870AA78E90

# Files:
- krevetka.py:
Code for the chess engine.
- main.py:
The file displaying the graphical user interface.
- endgame.mp3: 
This playlist is "Hard as Steel" by Abbynoise, and it is a Non-Copyright Song(NCS). It can be played after the game has ended.
- tools.py: 
Provides necessary "tools" for analyzing the screen, such as taking screenshots, finding positions, and moving the mouse to play.
- README.md: 
The file that you are currently reading.

# Lichess account:
⚠WARNING⚠: NOTE THAT ANYONE USING THIS BOT FOR CHEATING WILL BE BANNED(quiet logic I think). EVEN THOUGH YOU ARE USING IT WITH A LICHESS BOT ACCOUNT, YOU MUST KNOW THAT THIS BOT DOES NOT USE THE LICHESS API, AND FOR THAT REASON THIS BOT WILL BREAK THE TERMS OF SERVICE OF LICHESS.
(note that I am working on the implementation of the lichess API, so be patient)
PS: note also that using bots on online chess platforms is considered as cheating.

here: 👉https://lichess.org/@/KrevetkaBot (actually the bot was banned)
![game](https://user-images.githubusercontent.com/104983707/170866422-873fb47d-0310-46db-b7e9-55fbe7cb5910.gif)

# Run it!
run this command in the cmd: pip install -r requirements.txt

You must run the main.py file, if you want to play with the GUI(You can play without AI in the command just by running the krevetka.py file). I will also recommend to run it with the python interpreter pypy(here 👉 https://www.pypy.org/), dividing by two the waiting time(maximum 60s without, vs 30s with)).


(PS: There is a lot of code that is redundant and there are tons of improvements that can be made.)
