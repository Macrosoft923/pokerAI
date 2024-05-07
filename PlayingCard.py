import random

import timeout_decorator


class PlayingCard:
    def __init__(self):
        """
        トランプのカードを表すクラスです。

        Attributes:
        - data (list): カードのデータを格納した2次元リスト
        - counter (list): カードの使用状況を管理する2次元リスト
        """
        # self.data = [
        #     ['A♤', '2♤', '3♤', '4♤', '5♤', '6♤', '7♤',
        #         '8♤', '9♤', '10♤', 'J♤', 'Q♤', 'K♤'],
        #     ['A♢', '2♢', '3♢', '4♢', '5♢', '6♢', '7♢',
        #         '8♢', '9♢', '10♢', 'J♢', 'Q♢', 'K♢'],
        #     ['A♡', '2♡', '3♡', '4♡', '5♡', '6♡', '7♡',
        #         '8♡', '9♡', '10♡', 'J♡', 'Q♡', 'K♡'],
        #     ['A♧', '2♧', '3♧', '4♧', '5♧', '6♧', '7♧',
        #         '8♧', '9♧', '10♧', 'J♧', 'Q♧', 'K♧']
        # ]
        self.suits = ['♤', '♢', '♡', '♧']
        self.numbers = ['A', '2', '3', '4', '5',
                        '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.counter = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    @timeout_decorator.timeout(5)
    def getCard(self, cards):
        """
        ランダムにカードを取得します。

        Returns:
        - card (list): 取得したカードのリスト
        """
        card = []

        while len(card) < cards:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if self.counter[suit][number] == 1:
                # card.append(self.data[suit][number])
                card.append(dict(suit=suit, number=number))
                self.counter[suit][number] = 0

        return card
