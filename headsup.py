import numpy as np
import random

winner = None
players = 2

SUITS = ("♠", "♣", "♢", "♡")
NUMBERS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
LEN_SUITS = len(SUITS)
LEN_NUMBERS = len(NUMBERS)

cards = np.ones((LEN_SUITS, LEN_NUMBERS), dtype=int)
CARDS_COMMUNITY = np.zeros((LEN_SUITS, LEN_NUMBERS), dtype=int)
CARDS_HOLE = np.zeros((players, LEN_SUITS, LEN_NUMBERS), dtype=int)

SUM_CARDS_COMMUNITY = 3
SUM_CARDS_HOLE = 2

POKER_HANDS = (
    "STRAIGHT_FLUSH",
    "FOUR_OF_A_KIND",
    "FULL_HOUSE",
    "FLUSH",
    "STRAIGHT",
    "THREE_OF_A_KIND",
    "TWO_PAIR",
    "ONE_PAIR",
    "HIGH_CARD",
)

def getpokerhand(cards):
    poker_hand = 1
    sum_suits = np.sum(cards, axis=1)
    sum_numbers = np.sum(cards, axis=0)

    judlist = []
    isonepair = False
    istwopair = False
    isthreeofakind = False
    isfourofakind = False

    def isflush(cards,judlist):
        if judlist[0] <=6:
            for i in range(LEN_SUITS):
                if sum(cards[i])>= 5:
                    judlist = [i for i, x in enumerate(cards[i]) if x == 1][:5]
                    judlist.insert(0,6)
        return judlist
    
    def isstraight(sum_numbers,judlist):
        for i in range(10):
            if all(sum_numbers[i-1:i+4]):
                for j in range(4):
                    if sum(cards[j][i-1:i+4]) == 5:
                        judlist = list(range(i-1,i+4))
                        judlist.insert(0,9)
                if judlist[0] <=5:
                    judlist = list(range(i-1,i+4))
                    judlist.insert(0,5)
        return judlist
    
    def countjudge(sum_numbers,judlist):
        if judlist[0] <=8:
            if 4 in sum_numbers:
                for i in range(4):
                    judlist.append(sum_numbers.index(4))
                kicker = len(sum_numbers) - 1 - next(i for i, x in enumerate(reversed(sum_numbers)) if x != 0)
                judlist.append(kicker)
                judlist.insert(0,8)
            elif 3 in sum_numbers:
                for i in range(3):
                    judlist.append(sum_numbers.index(3))
    if isonepair:
        poker_hand = 7
    elif istwopair:
        poker_hand = 6

    if isthreeofakind:
        poker_hand = 5

    if isfourofakind:
        poker_hand = 1

    if isflush(sum_suits) and isstraight(sum_numbers):
        poker_hand = 0
    elif isflush(sum_suits):
        poker_hand = 3
    elif isstraight(sum_numbers):
        poker_hand = 4

    return poker_hand