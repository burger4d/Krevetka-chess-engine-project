# Krevetka-chess-engine-project

![chess.gif]

A basic chess engine coded in python, with a GUI that enables you to use more advanced chess engines as bots.


# Why "Krevetka"?
Krevetka (or Креветка) means "shrimp".

# The "image recognition"
The bot captures a screenshot and searches each individual pixel for colors belonging to the chessboard. It then determines the chessboard's location on the screen, ensuring its complete visibility, and begins playing. The program continually scans for any color modifications on two squares, indicating a piece has been moved, and deduces the last move made. While you can change pieces, the program requires the colors to remain the same, and moving the chessboard or altering its size during the game is forbidden.

Currently, the bot is compatible with the following websites: 
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

# Lichess account (banned):
⚠WARNING⚠: CHEATING IS BAD
![game](https://user-images.githubusercontent.com/104983707/170866422-873fb47d-0310-46db-b7e9-55fbe7cb5910.gif)


