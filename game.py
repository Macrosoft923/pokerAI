import collections
import numpy as np
import pandas as pd
import random
import time

MIN_PLAYERS = 2
MAX_PLAYERS = 10
players = (MIN_PLAYERS + MAX_PLAYERS) // 2

PLAYERS = np.arange(players, dtype=int)
PLAYERS_ACTIVE = np.ones(players, dtype=bool)
PLAYERS_ALL_IN = np.zeros(players, dtype=bool)

BUTTON = random.randint(0, players - 1)

MIN_BET = 40

ROUNDS_KEY = ("PRE_FLOP", "FLOP", "TURN", "RIVER")
ROUNDS_VALUE = np.zeros(4, dtype=bool)
ROUNDS_VALUE[0] = True
LEN_ROUNDS_KEY = len(ROUNDS_KEY)

SUITS = ("♠", "♣", "♢", "♡")
NUMBERS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
LEN_SUITS = len(SUITS)
LEN_NUMBERS = len(NUMBERS)

CARDS_COUNTER = np.ones((LEN_SUITS, LEN_NUMBERS), dtype=int)
CARDS_COMMUNITY = np.zeros((LEN_SUITS, LEN_NUMBERS), dtype=int)
CARDS_HOLE = np.zeros((players, LEN_SUITS, LEN_NUMBERS), dtype=int)
CARDS_RANKED = np.arange(LEN_NUMBERS, dtype=int) + 1
SUM_CARDS_COMMUNITY = 3
SUM_CARDS_HOLE = 2

POKER_HANDS = (
    "HIGH_CARD",
    "ONE_PAIR",
    "TWO_PAIR",
    "THREE_OF_A_KIND",
    "STRAIGHT",
    "FLUSH",
    "FULL_HOUSE",
    "FOUR_OF_A_KIND",
    "STRAIGHT_FLUSH",
)


def isclosed(players_active, actions_counter, bets, stacks):
    if np.count_nonzero(players_active) < 2:
        return True

    if all([bet == bets[players_active][0] for bet in bets[players_active]]) and all(
        actions != 0 for actions in actions_counter[players_active]
    ):
        return True

    if all([stack == 0 for stack in stacks[players_active]]):
        return True


def getpokerhand(cards):
    sum_suits = np.sum(cards, axis=1)
    sum_numbers = np.sum(cards, axis=0)
    indexes = np.array([-1, -1])
    poker_hand = "HIGH_CARD"

    def isflush(sum_suits):
        for i in range(SUM_CARDS_COMMUNITY + SUM_CARDS_HOLE + 1):
            if np.count_nonzero(sum_suits == i) > 4:
                return True

    def isstraight(sum_numbers):
        sum_sequential = 0

        for i in range(LEN_NUMBERS - 1):
            if sum_numbers[i] != 0 and sum_numbers[i + 1] != 0:
                sum_sequential += 1
            else:
                sum_sequential = 0

            if sum_sequential > 3:
                return True

    def getcombination(sum_numbers, indexes, poker_hand):
        isonepair = False
        istwopair = False
        isthreeofakind = False
        isfourofakind = False

        if np.count_nonzero(sum_numbers == 2) == 1:
            isonepair = True

        if np.count_nonzero(sum_numbers == 2) == 2:
            istwopair = True

        if np.count_nonzero(sum_numbers == 3) == 1:
            isthreeofakind = True

        if np.count_nonzero(sum_numbers == 4) == 1:
            isfourofakind = True

        if isonepair:
            index = np.argwhere(sum_numbers == 2)
            indexes[0] = index.item(-1)
            poker_hand = "ONE_PAIR"

        if istwopair:
            index = np.argwhere(sum_numbers == 2)
            indexes[0] = index.item(-1)
            indexes[1] = index.item(-2)
            poker_hand = "TWO_PAIR"

        if isthreeofakind:
            index = np.argwhere(sum_numbers == 3)
            indexes[0] = index.item(-1)
            poker_hand = "THREE_OF_A_KIND"

        if isonepair and isthreeofakind:
            index = np.argwhere(sum_numbers == 2)
            indexes[0] = index.item(-1)
            index = np.argwhere(sum_numbers == 3)
            indexes[1] = index.item(-1)
            poker_hand = "FULL_HOUSE"

        if isfourofakind:
            index = np.argwhere(sum_numbers == 4)
            indexes[1] = index.item(-1)
            poker_hand = "FOUR_OF_A_KIND"

        return indexes, poker_hand

    def getstraight(sum_numbers, indexes):
        sum_sequential = 0

        for i in range(1, LEN_NUMBERS - 1):
            if sum_numbers[i - 1] != 0 and sum_numbers[i] != 0:
                sum_sequential += 1
                index = i
            else:
                sum_sequential = 0
                index = -1

            if sum_sequential > 3:
                index -= 4
                indexes[0] = max(indexes[0], index)

        return indexes

    indexes, poker_hand = getcombination(sum_numbers, indexes, poker_hand)

    if isstraight(sum_numbers):
        indexes = getstraight(sum_numbers, indexes)
        poker_hand = "STRAIGHT"

    if isflush(sum_suits):
        poker_hand = "FLUSH"

    if isflush(sum_suits) and isstraight(sum_numbers):
        indexes = getstraight(sum_numbers, indexes)
        poker_hand = "STRAIGHT_FLUSH"

    return indexes, poker_hand


def gethighesthand(cards, indexes, poker_hand):
    sum_numbers = np.sum(cards, axis=0)
    hands_zeros = np.zeros(LEN_NUMBERS, dtype=int)

    highest_hands = np.stack([sum_numbers, hands_zeros], axis=0)

    if poker_hand == "ONE_PAIR":
        highest_hands[1, indexes[0]] = 2
        highest_hands[0] -= highest_hands[1]

    elif poker_hand == "TWO_PAIR":
        highest_hands[1, indexes[0]] = 2
        highest_hands[1, indexes[1]] = 2
        highest_hands[0] -= highest_hands[1]

    elif poker_hand == "THREE_OF_A_KIND":
        highest_hands[1, indexes[0]] = 3
        highest_hands[0] -= highest_hands[1]

    elif poker_hand == "STRAIGHT" or poker_hand == "STRAIGHT_FLUSH":
        highest_hands[1, indexes[0] : indexes[0] + 5] = 1
        highest_hands[0] -= highest_hands[1]

    elif poker_hand == "FULL_HOUSE":
        highest_hands[1, indexes[0]] = 2
        highest_hands[1, indexes[1]] = 3
        highest_hands[0] -= highest_hands[1]

    elif poker_hand == "FOUR_OF_A_KIND":
        highest_hands[1, indexes[0]] = 4
        highest_hands[0] -= highest_hands[1]

    return highest_hands


def idpokerhand(poker_hand):
    poker_hands = np.array(POKER_HANDS)
    hand_where = np.where(poker_hands == poker_hand)
    hand_id = hand_where[0][0]
    return hand_id


print("=" * 90)
print()
print("Welcome to Texas hold 'em.py")
print()
print("~" * 90)
print()

for i in range(LEN_ROUNDS_KEY):
    bets = np.zeros(players, dtype=int)
    actions_counter = np.zeros(players, dtype=int)

    button = (BUTTON + i) % players
    blind_small = (button + 1) % players
    blind_big = (button + 2) % players

    if ROUNDS_KEY[i] == "PRE_FLOP":
        winner = None

        pots = np.zeros(LEN_ROUNDS_KEY, dtype=int)

        bets[blind_small] += MIN_BET // 2
        bets[blind_big] += MIN_BET

        stacks = np.ones(players, dtype=int) * MIN_BET * 100
        stacks[blind_small] -= MIN_BET // 2
        stacks[blind_big] -= MIN_BET

        for j in range(players):
            while np.count_nonzero(CARDS_HOLE[j]) < SUM_CARDS_HOLE:
                suit = random.randint(0, 3)
                number = random.randint(0, 12)

                if CARDS_COUNTER[suit, number] == 1:
                    CARDS_HOLE[j, suit, number] = 1
                    CARDS_COUNTER[suit, number] = 0
                else:
                    continue

    elif ROUNDS_KEY[i] == "FLOP":
        while np.count_nonzero(CARDS_COMMUNITY) < SUM_CARDS_COMMUNITY:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if CARDS_COUNTER[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                CARDS_COUNTER[suit, number] = 0

        SUM_CARDS_COMMUNITY += 1

    elif ROUNDS_KEY[i] == "TURN":
        while np.count_nonzero(CARDS_COMMUNITY) < SUM_CARDS_COMMUNITY:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if CARDS_COUNTER[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                CARDS_COUNTER[suit, number] = 0

        SUM_CARDS_COMMUNITY += 1

    else:
        while np.count_nonzero(CARDS_COMMUNITY) < SUM_CARDS_COMMUNITY:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if CARDS_COUNTER[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                CARDS_COUNTER[suit, number] = 0

    min_bet = np.min(bets)
    max_bet = np.max(bets)
    sum_bet = np.sum(bets)

    print(
        f"information\t:round:\033[34m{ROUNDS_KEY[i]}\033[0m, players:\033[32m{players}\033[0m, button:\033[32m{button}\033[0m, small blind:\033[32m{blind_small}\033[0m, big blind:\033[32m{blind_big}\033[0m"
    )
    np.set_printoptions(formatter={"int": lambda x: f"${x}"})
    print(f"pots\t\t:{pots}")
    print(f"bets\t\t:{bets}")
    print(f"stacks\t\t:{stacks}")
    np.set_printoptions(formatter={"int": None})
    print(f"actions counter\t:{actions_counter}")
    print(f"active players\t:{PLAYERS_ACTIVE}")
    print(f"all in players\t:{PLAYERS_ALL_IN}")
    print()
    print("-" * 90)
    print()

    if ROUNDS_KEY[i] == "PRE_FLOP":
        for j in range(players):
            for k in range(LEN_SUITS):
                if k == 0:
                    print(f"hole cards[{j}]\t:{CARDS_HOLE[j, 0]}")
                else:
                    print(f"\t\t:{CARDS_HOLE[j, k]}")

            print()

    else:
        for j in range(LEN_SUITS):
            if j == 0:
                print(f"community cards\t:{CARDS_COMMUNITY[0]}")
            else:
                print(f"\t\t:{CARDS_COMMUNITY[j]}")

        print()

    print("-" * 90)
    print()

    while ROUNDS_VALUE[i]:
        for j in range(players):
            player = (j + button + 3) % players

            betting_options = np.empty(0, dtype=str)
            betting_options = np.append(betting_options, "FOLD")

            if i < 3 and isclosed(PLAYERS_ACTIVE, actions_counter, bets, stacks):
                ROUNDS_VALUE[i] = False
                ROUNDS_VALUE[i + 1] = True
                pots[i] = sum_bet
                break

            elif i == 3 and isclosed(PLAYERS_ACTIVE, actions_counter, bets, stacks):
                ROUNDS_VALUE[i] = False
                pots[i] = sum_bet
                break

            if not PLAYERS_ACTIVE[player]:
                continue

            if min_bet == max_bet:
                betting_options = np.append(betting_options, "CHECK")
            else:
                betting_options = np.append(betting_options, "CALL")

            if np.count_nonzero(bets) == 0:
                betting_options = np.append(betting_options, "BET")
            elif 2 * max_bet - bets[player] < stacks[player]:
                betting_options = np.append(betting_options, "RAISE")

            if (
                np.count_nonzero(PLAYERS_ALL_IN) > 0
                or max_bet - bets[player] > stacks[player]
            ):
                betting_options = np.array(["FOLD", "ALL_IN"])

            betting_option = random.choices(betting_options)[0]

            if betting_option == "CHECK":
                bet = 0
                bets[player] += bet
                stacks[player] -= bet
                actions_counter[player] += 1

            elif betting_option == "CALL":
                bet = max_bet - bets[player]
                bets[player] += bet
                stacks[player] -= bet
                actions_counter[player] += 1

            elif betting_option == "BET":
                bet = MIN_BET
                bets[player] += bet
                stacks[player] -= bet
                actions_counter[player] += 1

            elif betting_option == "RAISE":
                bet = random.randrange(
                    2 * max_bet - bets[player],
                    2 * max_bet + sum_bet - bets[player],
                    5,
                )
                bets[player] += bet
                stacks[player] -= bet
                actions_counter[player] += 1

            elif betting_option == "ALL_IN":
                PLAYERS_ALL_IN[player] = True
                bet = stacks[player] - bets[player]
                bets[player] += bet
                stacks[player] -= bet
                actions_counter[player] += 1

            else:
                PLAYERS_ACTIVE[player] = False
                bet = 0
                bets[player] += bet
                stacks[player] -= bet
                actions_counter[player] += 1

            min_bet = np.min(bets)
            max_bet = np.max(bets)
            sum_bet = np.sum(bets)

            print(
                f"information\t:player:\033[31m{player}\033[0m, betting option:\033[31m{betting_option}\033[0m, bet:\033[31m{bet}\033[0m, min bet:\033[31m{min_bet}\033[0m, max bet:\033[31m{max_bet}\033[0m, sum bet:\033[31m{sum_bet}\033[0m"
            )
            print(f"betting options\t:{betting_options}")
            np.set_printoptions(formatter={"int": lambda x: f"${x}"})
            print(f"bets\t\t:{bets}")
            print(f"stacks\t\t:{stacks}")
            np.set_printoptions(formatter={"int": None})
            print(f"actions counter\t:{actions_counter}")
            print(f"active players\t:{PLAYERS_ACTIVE}")
            print(f"all in players\t:{PLAYERS_ALL_IN}")
            print()

    if ROUNDS_KEY[i] == "RIVER":
        print("-" * 90)
        print()

        CARDS_HOLE += CARDS_COMMUNITY

        data = np.empty(0, dtype=int)

        for j in range(players):
            indexes, hand_poker = getpokerhand(CARDS_HOLE[j])
            hand_highest = gethighesthand(CARDS_HOLE[j], indexes, hand_poker)

            hand_id = idpokerhand(hand_poker)
            hand_point = np.sum(hand_highest[0] * CARDS_RANKED)

            information = np.array([indexes[0], indexes[1], hand_id, hand_point])
            data = np.append(data, information)

            print(f"poker hand[{j}]\t:{hand_poker}")
            print()
            print(f"highest hand[{j}]\t:{hand_highest[0]}")
            print(f"\t\t:{hand_highest[1]}")
            print()

            for k in range(LEN_SUITS):
                if k == 0:
                    print(f"hole cards[{j}]\t:{CARDS_HOLE[j, 0]}")
                else:
                    print(f"\t\t:{CARDS_HOLE[j, k]}")

            print()

        # remaining_players = PLAYERS[PLAYERS_ACTIVE]
        # remaining_poker_hands = poker_hands[PLAYERS_ACTIVE]

        # min_remaining_hands = np.min(remaining_poker_hands)

        # winner = remaining_poker_hands[remaining_poker_hands == min_remaining_hands]

        # print(remaining_poker_hands)
        # print(remaining_players)
        # print(winner)

        data = data.reshape([players, 4])
        dataframe = pd.DataFrame(
            data,
            columns=["indexes[0]", "indexes[1]", "hand_id", "hand_point"],
            index=[
                "player_1",
                "player_2",
                "player_3",
                "player_4",
                "player_5",
                "player_6",
            ],
        )

        print(dataframe)
        print()

    print("~" * 90)
    print()


print(f"winner\t\t:{winner}")
print(f"pots\t\t:{pots}")
print(f"active players\t:{PLAYERS_ACTIVE}")
print(f"all in players\t:{PLAYERS_ALL_IN}")
# print(f"players hands\t:{[POKER_HANDS[i] for i in poker_hands]}")
# print(f"winner hand\t:{POKER_HANDS[min_remaining_hands]}")

print()
print("=" * 90)
