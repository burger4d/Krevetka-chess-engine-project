# Krevetka-chess-engine-project
A basic chess engine coded in python using the python library chess.

Screenshot
![Capture](https://user-images.githubusercontent.com/104983707/166911776-a3860ced-65a5-4b0e-94ce-0bae0b65a930.PNG)


# Why Krevetka?
The name "Krevetka" means 🍤"shrimp"🦐.
It is in the same spirit like other chess engines, for example Rybka ("Rybka" means "fish"🐟)

# algorithm:
Wikipedia's definition: Minimax is a decision rule used in artificial intelligence, decision theory, game theory, statistics, and philosophy for minimizing the possible loss for a worst case (maximum loss) scenario. When dealing with gains, it is referred to as "maximin"—to maximize the minimum gain. Originally formulated for n-player zero-sum game theory, covering both the cases where players take alternate moves and those where they make simultaneous moves, it has also been extended to more complex games and to general decision-making in the presence of uncertainty.

I didn't do the algorithm in its recursive version, but only with some "for" loops(faster).


# opening book
from here: 👉 https://www.chessprogramming.net/new-version-of-the-baron-v3-43-plus-the-barons-polyglot-opening-book/?adlt=strict&toWww=1&redig=77DC80D3A2ED4E94A5CFD6733F2CC5B2

# lichess account
here: 👉https://lichess.org/@/KrevetkaBot

# Run it!
You must run the main.py file, if you want to play with the GUI(You can play without AI just by running the krevetka.py file). I will also recommend to run it with the python interpreter pypy(here => https://www.pypy.org/), dividing by two the waiting time(maximum 60s without, vs 30s with).

(PS: There are a lot of code that are redundant and there are tons of improvements that can be made.)
