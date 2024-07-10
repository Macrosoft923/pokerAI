import numpy as np
import random

MIN_PLAYERS = 2
MAX_PLAYERS = 10
PLAYERS = (MIN_PLAYERS + MAX_PLAYERS) // 2

BUTTON = random.randint(0, PLAYERS - 1)

print(BUTTON)

CARDS = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1])

NUMBERS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
LEN_NUMBERS = len(NUMBERS)


def isstraight_(sum_numbers):
    sum_sequential = 0

    for i in range(LEN_NUMBERS - 1):
        if sum_numbers[i] != 0 and sum_numbers[i + 1] != 0:
            sum_sequential += 1
        else:
            sum_sequential = 0

        if sum_sequential > 3:
            return True


def isstraight(sum_numbers):
    sum_sequential = 0

    for i in range(LEN_NUMBERS - 1):
        j = (i + 12) % LEN_NUMBERS
        k = (i + 13) % LEN_NUMBERS

        if sum_numbers[j] != 0 and sum_numbers[k] != 0:
            sum_sequential += 1
        else:
            sum_sequential = 0

        if sum_sequential > 3:
            return True


print(isstraight_(CARDS))
print(isstraight(CARDS))
