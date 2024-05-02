import random

import timeout_decorator


class PlayingCard:
    def __init__(self):
        self.data = [
            ['A♤', '2♤', '3♤', '4♤', '5♤', '6♤', '7♤',
                '8♤', '9♤', '10♤', 'J♤', 'Q♤', 'K♤'],
            ['A♢', '2♢', '3♢', '4♢', '5♢', '6♢', '7♢',
                '8♢', '9♢', '10♢', 'J♢', 'Q♢', 'K♢'],
            ['A♡', '2♡', '3♡', '4♡', '5♡', '6♡', '7♡',
                '8♡', '9♡', '10♡', 'J♡', 'Q♡', 'K♡'],
            ['A♧', '2♧', '3♧', '4♧', '5♧', '6♧', '7♧',
                '8♧', '9♧', '10♧', 'J♧', 'Q♧', 'K♧']
        ]
        self.counter = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    @timeout_decorator.timeout(5)
    def getCard(self):
        card = []

        while len(card) == 0:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if self.counter[suit][number] == 1:
                card.append(self.data[suit][number])
                self.counter[suit][number] = 0

        return card
