import collections
import itertools
import numpy as np
import random
import time


def pokerhands(cards):
    sum_suits = np.sum(cards, axis=1)
    sum_numbers = np.sum(cards, axis=0)

    counter_suits = collections.Counter(sum_suits)
    counter_numbers = collections.Counter(sum_numbers)

    if counter_numbers[2] == 1:
        return "ONE PAIR"
    elif counter_numbers[2] == 2:
        return "TWO PAIR"
    elif counter_numbers[3] == 1:
        return "THREE OF A KIND"
    elif counter_numbers[3] == 1 and counter_numbers[2] == 1:
        return "FULL HOUSE"
    elif counter_numbers[4] == 1:
        return "FOUR OF A KIND"
    elif counter_suits[5] == 1:
        return "FLUSH"
    elif counter_numbers[5] == 1:
        return "STRAIGHT"
    else:
        return "HIGH CARD"


cards = np.ones((4, 13), dtype=int)
CARDS_COMMUNITY = np.zeros((4, 13), dtype=int)
CARDS_HOLE = np.zeros((6, 4, 13), dtype=int)

for j in range(6):
    while np.count_nonzero(CARDS_HOLE[j]) < 2:
        suit = random.randint(0, 3)
        number = random.randint(0, 12)

        if cards[suit, number] == 1:
            CARDS_HOLE[j, suit, number] = 1
            cards[suit, number] = 0

while np.count_nonzero(CARDS_COMMUNITY) < 5:
    suit = random.randint(0, 3)
    number = random.randint(0, 12)

    if cards[suit, number] == 1:
        CARDS_COMMUNITY[suit, number] = 1
        cards[suit, number] = 0

CARDS_HOLE += CARDS_COMMUNITY

# for j in range(6):
#     SUM_SUITS = np.sum(CARDS_HOLE[j], axis=1)
#     SUM_NUMBERS = np.sum(CARDS_HOLE[j], axis=0)
#     counter_suits = collections.Counter(SUM_SUITS)
#     counter_numbers = collections.Counter(SUM_NUMBERS)

#     print(pokerhands(CARDS_HOLE[j]))
#     print(SUM_SUITS)
#     print(SUM_NUMBERS)
#     print(counter_suits)
#     print(counter_numbers)
#     print()

SUM_NUMBERS = np.array([0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1])
print(list(itertools.combinations(range(13), 5)))
