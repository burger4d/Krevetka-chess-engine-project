# Krevetka-chess-engine-project
A basic chess engine coded in python.

Screenshot
![Capture](https://user-images.githubusercontent.com/104983707/166911776-a3860ced-65a5-4b0e-94ce-0bae0b65a930.PNG)


# Why Krevetka?
The name "Krevetka" means 🍤"shrimp"🦐.
It is in the same spirit like other chess engines, for example Rybka or stockfish (note that "Rybka" means "fish"🐟)

# The algorithm:
Wikipedia's definition: Minimax is a decision rule used in artificial intelligence, decision theory, game theory, statistics, and philosophy for minimizing the possible loss for a worst case (maximum loss) scenario. When dealing with gains, it is referred to as "maximin"—to maximize the minimum gain. Originally formulated for n-player zero-sum game theory, covering both the cases where players take alternate moves and those where they make simultaneous moves, it has also been extended to more complex games and to general decision-making in the presence of uncertainty.

Krevetka uses this algorithm, with a depth of 3. I didn't do the algorithm in its recursive version, but only with some "for" loops(faster).

# Files:
-baron30.bin:
A polyglot opening book, from here: 👉 https://www.chessprogramming.net/new-version-of-the-baron-v3-43-plus-the-barons-polyglot-opening-book/?adlt=strict&toWww=1&redig=77DC80D3A2ED4E94A5CFD6733F2CC5B2

-krevetka.py:
The code of the chess engine.

-main.py:
The file with the GUI.

-online_sources.py:
This file is a homemade API. The AI can have access to the endgame tablebase syzygy (here👉https://syzygy-tables.info/?adlt=strict&toWww=1&redig=7B4251AD8D5542B89B81810568F3680B), and can also play game against someone on lichess, just by pasting the url of the game(I didn't use the LichessAPI, due to the procrastinization when I must read its documentation and also because I wanted to improve my skills in python, with urllib and pyautogui).

-README.md:
The file that you are currently reading.

# Lichess account:
here: 👉https://lichess.org/@/KrevetkaBot
![game](https://user-images.githubusercontent.com/104983707/170866422-873fb47d-0310-46db-b7e9-55fbe7cb5910.gif)

# Run it!
Requirements: Python 3.7+, python chess library(here 👉 https://pypi.org/project/chess/?adlt=strict&toWww=1&redig=9D7008CF0644473BB6615ACF0B8959C2), pyautogui(here 👉https://pypi.org/project/PyAutoGUI/?adlt=strict&toWww=1&redig=51B1DB6A75634B18B9BCBF57E7D5375B)

You must run the main.py file, if you want to play with the GUI(You can play without AI in the command just by running the krevetka.py file). I will also recommend to run it with the python interpreter pypy(here 👉 https://www.pypy.org/), dividing by two the waiting time(maximum 60s without, vs 30s with)).


(PS: There are a lot of code that are redundant and there are tons of improvements that can be made.)
