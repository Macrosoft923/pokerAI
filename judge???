import random

import timeout_decorator


class PlayingCard:
    def __init__(self,num):
        """
        トランプのカードを表すクラスです。

        Attributes:
        - data (list): カードのデータを格納した2次元リスト
        - counter (list): カードの使用状況を管理する2次元リスト
        """
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
        self.num = num

    @timeout_decorator.timeout(5)
    def getCard(self):
        """
        ランダムにカードを取得します。

        Returns:
        - card (list): 取得したカードのリスト
        """
        card = []

        while len(card) < 7:
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            if self.counter[suit][number] == 1:
                card.append(self.data[suit][number])
                self.counter[suit][number] = 0

        return card
    def comcard(self):
        comcard = []
        while len(comcard) < 5:
              suit = random.randint(0, 3)
              number = random.randint(0, 12)

              if self.counter[suit][number] == 1:
                  comcard.append(self.data[suit][number])
                  self.counter[suit][number] = 0
    def plycard(self):
        plycard = [[],[],[],[],[],[],[],[]]
        for i in range(self.num):
          while len(plycard[i]) < 2:
                suit = random.randint(0, 3)
                number = random.randint(0, 12)

                if self.counter[suit][number] == 1:
                    plycard[i].append(self.data[suit][number])
                    self.counter[suit][number] = 0
    def judge(self):
        many = [{},{},{},{},{},{},{},{}]#要素数
        judge = [[],[],[],[],[],[],[],[]]#約判定リスト
        num = self.num
        for i in range(num):
          self.plycard[num].append(self.comcard)
          revply = sorted(self.plycard[i], reverse=True)#降順に並べた
          for j in revply:
            many[i][j] = revply[i][j].count
          for k in many[i]:
            if many[i][k] == 3:
              judge[i].append(104)
              judge[i].append(i)
            elif many[i][k] == 2:
              judge[i].append(102)
              judge[i].append(k)

            elif many[i][k] == 4:
              pass
            if judge[i].count(102) >=2:
              judge[i][0] = 103
            if 102 in judge[i]:
              if 104 in judge[i]:
                judge[i][0] = 106
          if not judge[i]:
            judge[i] = revply[i]
          for l in many[i]:
            if many[l] == 1:
              judge[i].append(l)
        return judge
