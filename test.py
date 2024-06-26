import numpy as np

while np.count_nonzero(CARDS_HOLE[j]) < SUM_CARDS_HOLE:
    suit = random.randint(0, 3)
    number = random.randint(0, 12)

    if CARDS_COUNTER[suit, number] == 1:
        CARDS_HOLE[j, suit, number] = 1
        CARDS_COUNTER[suit, number] = 0
    else:
        continue
