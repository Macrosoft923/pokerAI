import numpy as np
import random
import time

MIN_PLAYERS = 2
MAX_PLAYERS = 10
players = (MIN_PLAYERS + MAX_PLAYERS) // 2

ACTIVE_PLAYERS = np.ones(players, dtype=bool)

BUTTON = random.randint(0, players - 1)
winner = None

MIN_BET = 40
POT = 0

SUITS = ("♠", "♣", "♢", "♡")
NUMBERS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
cards = np.ones((4, 13))

CARDS_COMMUNITY = np.zeros((4, 13))
CARDS_HOLE = np.zeros((players, 4, 13))


def isclosed(active_players, pots, stacks):
    if np.count_nonzero(active_players) == 0:
        return True
    if all(
        [
            pot == pots[active_players][0] and pots[active_players][0] != 0
            for pot in pots[active_players]
        ]
    ):
        return True
    if all([stack == 0 for stack in stacks[active_players]]):
        return True


print("=" * 100)
print()
print("Welcome to Texas hold 'em.py")
print()
print("-" * 100)
print()

ROUNDS_KEY = ("PRE_FLOP", "FLOP", "TURN", "RIVER")
ROUNDS_VALUE = np.zeros(4, dtype=bool)
ROUNDS_VALUE[0] = True

for i in range(4):
    button = (BUTTON + i) % players
    blind_small = (button + 1) % players
    blind_big = (button + 2) % players

    if ROUNDS_KEY[i] == "PRE_FLOP":
        pots = np.zeros(players, dtype=np.int64)
        pots[blind_small] += MIN_BET // 2
        pots[blind_big] += MIN_BET

        stacks = np.ones(players, dtype=np.int64) * MIN_BET * 100
        stacks[blind_small] -= MIN_BET // 2
        stacks[blind_big] -= MIN_BET

        for j in range(players):
            while np.count_nonzero(CARDS_HOLE[j]) < 2:
                suit = random.randint(0, 3)
                number = random.randint(0, 12)

                if cards[suit, number] == 1:
                    CARDS_HOLE[j, suit, number] = 1
                    cards[suit, number] == 0

    elif ROUNDS_KEY[i] == "FLOP":
        pots = np.zeros(players, dtype=int)

        while np.count_nonzero(CARDS_COMMUNITY) < 3:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if cards[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                cards[suit, number] == 0

    elif ROUNDS_KEY[i] == "TURN":
        pots = np.zeros(players, dtype=int)

        while np.count_nonzero(CARDS_COMMUNITY) < 4:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if cards[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                cards[suit, number] == 0

    else:
        pots = np.zeros(players, dtype=int)

        while np.count_nonzero(CARDS_COMMUNITY) < 5:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if cards[suit, number] == 1:
                CARDS_COMMUNITY[suit, number] = 1
                cards[suit, number] == 0

    min_bet = min(pots)
    max_bet = max(pots)
    sum_bet = sum(pots)

    print(
        f"information\t:round:\033[34m{ROUNDS_KEY[i]}\033[0m, players:\033[32m{players}\033[0m, button:\033[32m{button}\033[0m, small blind:\033[32m{blind_small}\033[0m, big blind:\033[32m{blind_big}\033[0m, pot:\033[32m{POT}\033[0m"
    )
    print(f"pots\t\t:{pots}")
    print(f"stacks\t\t:{stacks}")
    print(f"active players\t:{ACTIVE_PLAYERS}")
    print()

    if ROUNDS_KEY[i] == "PRE_FLOP":
        for j in range(players):
            for k in range(4):
                if j == 0 and k == 0:
                    print(f"hole cards\t:{CARDS_HOLE[0][0]}")
                else:
                    print(f"\t\t:{CARDS_HOLE[j][k]}")

            print()

    else:
        for j in range(4):
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

            if i < 3 and isclosed(ACTIVE_PLAYERS, pots, stacks):
                ROUNDS_VALUE[i] = False
                ROUNDS_VALUE[i + 1] = True
                POT += sum_bet
                break

            elif i == 3 and isclosed(ACTIVE_PLAYERS, pots, stacks):
                ROUNDS_VALUE[i] = False
                POT += sum_bet
                break

            if not ACTIVE_PLAYERS[player]:
                continue

            if min_bet == max_bet:
                betting_options = np.append(betting_options, "CHECK")

            if min_bet != max_bet:
                betting_options = np.append(betting_options, "CALL")

            if np.count_nonzero(pots) == 0:
                betting_options = np.append(betting_options, "BET")

            if np.count_nonzero(pots) != 0:
                betting_options = np.append(betting_options, "RAISE")

            betting_option = random.choices(betting_options)[0]

            if betting_option == "CHECK":
                bet = 0
                pots[player] += bet
                stacks[player] -= bet

            elif betting_option == "CALL" and max_bet - pots[player] < stacks[player]:
                bet = max_bet - pots[player]
                pots[player] += bet
                stacks[player] -= bet

            elif betting_option == "CALL":
                ACTIVE_PLAYERS[player] = False
                betting_option = "ALL_IN"
                bet = stacks[player] - pots[player]
                pots[player] += bet
                stacks[player] -= bet

            elif betting_option == "BET":
                bet = MIN_BET
                pots[player] += bet
                stacks[player] -= bet

            elif betting_option == "RAISE" and (
                (2 * max_bet - pots[player])
                < 2 * max_bet + sum_bet - pots[player]
                < stacks[player]
            ):
                bet = random.randrange(
                    2 * max_bet - pots[player],
                    2 * max_bet + sum_bet - pots[player],
                    5,
                )
                pots[player] += bet
                stacks[player] -= bet

            elif betting_option == "RAISE":
                ACTIVE_PLAYERS[player] = False
                betting_option = "ALL_IN"
                bet = stacks[player] - pots[player]
                pots[player] += bet
                stacks[player] -= bet

            else:
                ACTIVE_PLAYERS[player] = False
                bet = 0
                pots[player] += bet
                stacks[player] -= bet

            min_bet = min(pots)
            max_bet = max(pots)
            sum_bet = sum(pots)

            print(
                f"information\t:player:\033[31m{player}\033[0m, betting option:\033[31m{betting_option}\033[0m, bet:\033[31m{bet}\033[0m, min bet:\033[31m{min_bet}\033[0m, max bet:\033[31m{max_bet}\033[0m, sum bet:\033[31m{sum_bet}\033[0m"
            )
            print(f"betting options\t:{betting_options}")
            print(f"pots\t\t:{pots}")
            print(f"stacks\t\t:{stacks}")
            print(f"active players\t:{ACTIVE_PLAYERS}")
            print()

            if np.count_nonzero(ACTIVE_PLAYERS) == 1:
                winner = np.arange(players)[ACTIVE_PLAYERS][0]
                ROUNDS_VALUE[i] = False
                break

    # このゲームの目的は、ポット（pot, 全員の賭け金を集めたもの）を獲得することにある。ポットを獲得するためには、ショーダウンの際に最も強い5枚のカードを持つか、中途のベットラウンドにおいて他のプレイヤーを勝負から降ろす（フォルドさせる）必要がある。

    if ROUNDS_KEY[i] == "RIVER":
        CARDS_HOLE += CARDS_COMMUNITY

        for j in range(players):
            SUM_SUITS = np.sum(CARDS_HOLE[j], axis=1)
            SUM_NUMBERS = np.sum(CARDS_HOLE[j], axis=0)

            print(f"sum suits[{j}]\t:{SUM_SUITS}")
            print(f"sum numbers[{j}]\t:{SUM_NUMBERS}")
            print()

    print("-" * 100)
    print()


print(f"winner\t\t:{winner}")
print(f"pot\t\t:{POT}")
print(f"active players\t:{ACTIVE_PLAYERS}")

print()
print("=" * 100)
