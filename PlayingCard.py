import numpy as np
import random


class PlayingCard:
    def __init__(self):
        """トランプのデッキを表す PlayingCard オブジェクトを初期化します。

        Attributes:
            counter (list): 各カードの利用可能性を表す2次元リスト
        """
        # 52枚のカード (4スーツ x 13ランク) の存在を示す2次元リストを初期化
        self.counter = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def get_card(self):
        """デッキから指定された枚数のランダムなカードを引きます。

        Returns:
            card (list): カードを表す辞書のリスト
        """
        card = []

        while len(card) < 1:
            # スーツとランクをランダムに選択
            suit = random.randint(0, 3)
            number = random.randint(0, 12)

            # 選択したカードが利用可能ならば、カードリストに追加し利用不可に設定
            if self.counter[suit][number] == 1:
                card.append(dict(suit=suit, number=number))
                self.counter[suit][number] = 0

        return card

    def get_cards(self, N):
        """デッキから指定された枚数のランダムなカードを引きます。

        Args:
            N (int): 引くカードの枚数

        Returns:
            cards (list): カードを表す辞書のリスト
        """
        cards = []

        while len(cards) < N:
            # スーツとランクをランダムに選択
            suit = random.randint(0, 3)
            number = random.randint(0, 12)
            card = 13 * suit + number  # カードを一意に識別するための値に変換

            # 選択したカードが利用可能ならば、カードリストに追加し利用不可に設定
            if self.counter[suit][number] == 1:
                cards.append(card)
                self.counter[suit][number] = 0

        return cards

    def get_dealer_cards(self):
        """デッキから5枚のランダムなカードを引きます。

        Returns:
            dealercards (list): ディーラーの手札を表すカードのリスト
        """
        # ディーラーの手札として5枚のカードを取得
        dealercards = self.get_cards(5)

        return dealercards

    def get_player_hands(self, dealercards, N):
        """デッキから指定された人数のランダムなカードを引きます。

        Args:
            dealercards (list): ディーラーの手札を表すカードのリスト
            N (int): 引くカードの人数

        Returns:
            playerhands (ndarray): プレイヤーの手札を表す4次元配列
        """
        # プレイヤーの手札を保存するための4次元配列を作成
        playerhands = np.zeros((N, 4, 13))

        # for i in range(N):
        #     for dealercard in dealercards:
        #         # カード番号をスートとランクに分解
        #         suit = dealercard // 13
        #         number = dealercard % 13

        #         for j in range(4):
        #             for k in range(13):
        #                 # 該当するスートとランクの位置に1を設定
        #                 if j == suit and k == number:
        #                     playerhands[i, j, k] = 1
        #                 else:
        #                     continue

        for i in range(N):
            # 各プレイヤーに2枚のカードを配布
            playercards = self.get_cards(2)

            for playercard in playercards:
                # カード番号をスートとランクに分解
                suit = playercard // 13
                number = playercard % 13

                for j in range(4):
                    for k in range(13):
                        # 該当するスートとランクの位置に1を設定
                        if j == suit and k == number:
                            playerhands[i, j, k] = 1
                        else:
                            continue

        return playerhands
