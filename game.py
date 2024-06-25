import collections
import numpy as np
import random
import time

MIN_PLAYERS = 2
MAX_PLAYERS = 10
players = (MIN_PLAYERS + MAX_PLAYERS) // 2

PLAYERS = np.arange(players, dtype=int)
PLAYERS_ACTIVE = np.ones(players, dtype=bool)
PLAYERS_ALL_IN = np.zeros(players, dtype=bool)

BUTTON = random.randint(0, players - 1)

winner = None

MIN_BET = 40

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


def isclosed(players_active, actions_counter, bets, stacks):
    if np.count_nonzero(players_active) < 2:
        return True

    if all(
        [
            bet == bets[players_active][0] and actions_counter[players_active][0] != 0
            for bet in bets[players_active]
        ]
    ):
        return True

    if all([stack == 0 for stack in stacks[players_active]]):
        return True


def getpokerhand(cards):
    poker_hand = 8
    sum_suits = np.sum(cards, axis=1)
    sum_numbers = np.sum(cards, axis=0)

    isonepair = False
    istwopair = False
    isthreeofakind = False
    isfourofakind = False

    def isflush(sum_suits):
        for i in range(SUM_CARDS_COMMUNITY + SUM_CARDS_HOLE + 1):
            if np.count_nonzero(sum_suits == i) > 4:
                return True

    def isstraight(sum_numbers):
        sum_sequential = 0

        for i in range(LEN_NUMBERS - 1):
            if sum_numbers[i] > 0 and sum_numbers[i + 1] > 0:
                sum_sequential += 1
            else:
                sum_sequential = 0

            if sum_sequential > 3:
                return True

    for i in range(2, LEN_SUITS + 1):
        for j in range(1, (SUM_CARDS_COMMUNITY + SUM_CARDS_HOLE) // i):
            if np.count_nonzero(sum_numbers == i) == j:
                if i == 2 and j == 1:
                    isonepair = True
                elif i == 2:
                    isonepair = False
                    istwopair = True

                if i == 3:
                    isthreeofakind = True

                if i == 4:
                    isfourofakind = True

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


def gethighesthand(cards, poker_hand):
    # 続きは、ここから
    return


print("=" * 90)
print()
print("Welcome to Texas hold 'em.py")
print()
print("-" * 90)
print()

ROUNDS_KEY = ("PRE_FLOP", "FLOP", "TURN", "RIVER")
ROUNDS_VALUE = np.zeros(4, dtype=bool)
ROUNDS_VALUE[0] = True
LEN_ROUNDS_KEY = len(ROUNDS_KEY)

pots = np.zeros(LEN_ROUNDS_KEY, dtype=int)

for i in range(LEN_ROUNDS_KEY):
    button = (BUTTON + i) % players
    blind_small = (button + 1) % players
    blind_big = (button + 2) % players

    if ROUNDS_KEY[i] == "PRE_FLOP":
        actions_counter = np.zeros(players, dtype=int)

        bets = np.zeros(players, dtype=np.int64)
        bets[blind_small] += MIN_BET // 2
        bets[blind_big] += MIN_BET

        stacks = np.ones(players, dtype=np.int64) * MIN_BET * 100
        stacks[blind_small] -= MIN_BET // 2
        stacks[blind_big] -= MIN_BET

        for j in range(players):
            while np.count_nonzero(CARDS_HOLE[j]) < SUM_CARDS_HOLE:
                suit = random.randint(0, 3)
                number = random.randint(0, 12)

                if cards[suit, number] == 1:
                    CARDS_HOLE[j, suit, number] = 1
                    cards[suit, number] = 0

    elif ROUNDS_KEY[i] == "FLOP":
        actions_counter = np.zeros(players, dtype=int)

        bets = np.zeros(players, dtype=int)

        while np.count_nonzero(CARDS_COMMUNITY) < SUM_CARDS_COMMUNITY:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if cards[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                cards[suit, number] = 0

        SUM_CARDS_COMMUNITY += 1

    elif ROUNDS_KEY[i] == "TURN":
        actions_counter = np.zeros(players, dtype=int)

        bets = np.zeros(players, dtype=int)

        while np.count_nonzero(CARDS_COMMUNITY) < SUM_CARDS_COMMUNITY:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if cards[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                cards[suit, number] = 0

        SUM_CARDS_COMMUNITY += 1

    else:
        actions_counter = np.zeros(players, dtype=int)

        bets = np.zeros(players, dtype=int)

        while np.count_nonzero(CARDS_COMMUNITY) < SUM_CARDS_COMMUNITY:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if cards[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                cards[suit, number] = 0

    min_bet = min(bets)
    max_bet = max(bets)
    sum_bet = sum(bets)

    print(
        f"information\t:round:\033[34m{ROUNDS_KEY[i]}\033[0m, players:\033[32m{players}\033[0m, button:\033[32m{button}\033[0m, small blind:\033[32m{blind_small}\033[0m, big blind:\033[32m{blind_big}\033[0m"
    )
    print(f"pots\t\t:{pots}")
    print(f"bets\t\t:{bets}")
    print(f"stacks\t\t:{stacks}")
    print(f"actions counter\t:{actions_counter}")
    print(f"active players\t:{PLAYERS_ACTIVE}")
    print(f"all in players\t:{PLAYERS_ALL_IN}")
    print()

    if ROUNDS_KEY[i] == "PRE_FLOP":
        for j in range(players):
            for k in range(LEN_SUITS):
                if k == 0:
                    print(f"hole cards[{j}]\t:{CARDS_HOLE[0][0]}")
                else:
                    print(f"\t\t:{CARDS_HOLE[j][k]}")

            print()

    else:
        for j in range(LEN_SUITS):
            if j == 0:
                print(f"community cards\t:{CARDS_COMMUNITY[0]}")
            else:
                print(f"\t\t:{CARDS_COMMUNITY[j]}")

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
            else:
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

            min_bet = min(bets)
            max_bet = max(bets)
            sum_bet = sum(bets)

            print(
                f"information\t:player:\033[31m{player}\033[0m, betting option:\033[31m{betting_option}\033[0m, bet:\033[31m{bet}\033[0m, min bet:\033[31m{min_bet}\033[0m, max bet:\033[31m{max_bet}\033[0m, sum bet:\033[31m{sum_bet}\033[0m"
            )
            print(f"betting options\t:{betting_options}")
            print(f"bets\t\t:{bets}")
            print(f"stacks\t\t:{stacks}")
            print(f"actions counter\t:{actions_counter}")
            print(f"active players\t:{PLAYERS_ACTIVE}")
            print(f"all in players\t:{PLAYERS_ALL_IN}")
            print()

    # このゲームの目的は、ポット（pot, 全員の賭け金を集めたもの）を獲得することにある。ポットを獲得するためには、ショーダウンの際に最も強い5枚のカードを持つか、中途のベットラウンドにおいて他のプレイヤーを勝負から降ろす（フォルドさせる）必要がある。

    if ROUNDS_KEY[i] == "RIVER":
        print("-" * 90)
        print()

        CARDS_HOLE += CARDS_COMMUNITY

        for j in range(players):
            for k in range(LEN_SUITS):
                if k == 0:
                    print(f"hole cards[{j}]\t:{CARDS_HOLE[0][0]}")
                else:
                    print(f"\t\t:{CARDS_HOLE[j][k]}")

            print()

        players_hands = np.empty(0, dtype=int)
        players_highests = np.empty(0, dtype=int)

        for j in range(players):
            players_hand = getpokerhand(CARDS_HOLE[j])
            players_highest = gethighesthand(CARDS_HOLE[j], players_hand)

            players_hands = np.append(players_hands, players_hand)
            players_highests = np.append(players_highests, players_highest)

        remaining_hands = players_hands[PLAYERS_ACTIVE]
        remaining_players = PLAYERS[PLAYERS_ACTIVE]

        min_remaining_hands = np.min(remaining_hands)

        winner = remaining_hands[remaining_hands == min_remaining_hands]

        print(remaining_hands)
        print(remaining_players)
        print(winner)
        print()

    print("-" * 90)
    print()


print(f"winner\t\t:{winner}")
print(f"pots\t\t:{pots}")
print(f"active players\t:{PLAYERS_ACTIVE}")
print(f"all in players\t:{PLAYERS_ALL_IN}")
print(f"players hands\t:{[POKER_HANDS[i] for i in players_hands]}")
print(f"winner hand\t:{POKER_HANDS[min_remaining_hands]}")

print()
print("=" * 90)
