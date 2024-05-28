import numpy as np
from playingcard import PlayingCard as pc

pc = pc()

dealercards = pc.get_dealer_cards()
playerhands = pc.get_player_hands(dealercards, 10)

print(np.zeros(13))
