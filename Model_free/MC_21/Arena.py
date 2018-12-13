from Dealer import Dealer
from Player import Player
from queue import Queue
from random import shuffle
from typing import Iterable
from tqdm import tqdm


class Arena():

    def __init__(self, display=None, A=None):
        self.cards = ['A', '2', '3', '4', '5', '6',
                      '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        self.card_q = Queue(maxsize=52)
        self.cards_in_pool = []
        self.display = display
        self.episodes = []
        self.load_cards(self.cards)
        self.A = A

    def load_cards(self, cards):
        shuffle(cards)
        for card in cards:
            self.card_q.put(card)
        cards.clear()
        return

    def reward_of(self, dealer: Dealer, player: Player):
        dealer_points, _ = dealer.get_points()
        player_points, useable_ace = player.get_points()
        if player_points > 21:
            reward = -1
        else:
            if player_points > dealer_points or dealer_points > 21:
                reward = 1
            elif player_points == dealer_points:
                reward = 0
            else:
                reward = -1
        return reward, player_points, dealer_points, useable_ace

    def serve_card_to(self, player: Player, n=1):
        cards = []
        for _ in range(n):
            if self.card_q.empty():
                self._info('\nNo card in box, reshuffle cards.')
                shuffle(self.cards_in_pool)
                self._info('\nNow put {} cards in box.'.format(
                    len(self.cards_in_pool)))
                assert(len(self.cards_in_pool) > 20)
                self.load_cards(self.cards_in_pool)
            cards.append(self.card_q.get())
        self._info('\nSend {} cards ({}) to {}{}'.format(
            n, cards, player.role, player))
        player.receive(cards)
        player.cards_info()

    def _info(self, msg):
        if self.display:
            print(msg, end="")

    def recycle_cards(self, *players: Iterable[Player]):
        if len(players) == 0:
            return
        for player in players:
            for card in player.cards:
                self.cards_in_pool.append(card)
            player.discharge_cards()

    def play_game(self, dealer: Dealer, player: Player):
        self._info('\n===================New Game==================')
        self.serve_card_to(player, n=2)
        self.serve_card_to(dealer, n=2)
        episode = []
        if player.policy is None:
            self._info('\n Player need a policy.')
            return
        if dealer.policy is None:
            self._info('\n Dealer need a policy.')
            return
        while True:
            action = player.policy(dealer)
            self._info('{}{} choose: {};'.format(player.role, player, action))
            episode.append((player.get_state_name(dealer), action))
            if action == self.A[0]:
                self.serve_card_to(player)
            else:
                break

        reward, player_points, dealer_points, useable_ace = self.reward_of(
            dealer, player)

        if player_points > 21:
            self._info('\n Player lose {}, get score: {}'.format(
                player_points, reward))
            self.recycle_cards(player, dealer)
            self.episodes.append((episode, reward))
            self._info('\n =================End Game================')

            return episode, reward

        self._info('\n')
        while True:
            action = dealer.policy()
            self._info('\n {}{} choose: {};'.format(
                dealer.role, dealer, action))
            if action == self.A[0]:
                self.serve_card_to(dealer)
            else:
                break
        self._info('\nStop Choose;\n')
        reward, player_points, dealer_points, useable_ace = self.reward_of(
            dealer, player)
        player.cards_info()
        dealer.cards_info()
        if reward == +1:
            self._info('\nPlayer Win!')
        elif reward == -1:
            self._info('\nDealer Win!')
        else:
            self._info('\nPeace!')
        self._info("\nPlayer {}, Dealer {}".format(
            player_points, dealer_points))
        self._info('\n =================End Game================')
        self.recycle_cards(player, dealer)
        self.episodes.append((episode, reward))

        return episode, reward

    def play_games(self, dealer, player, num=2, show_statistic=True):
        '''一次性玩多局游戏
        '''
        results = [0, 0, 0]  # 玩家负、和、胜局数
        self.episodes.clear()
        for _ in tqdm(range(num)):
            episode, reward = self.play_game(dealer, player)
            results[1+reward] += 1
            if player.learning_method is not None:
                player.learning_method(episode, reward)
        if show_statistic:
            print("共玩了{}局，玩家赢{}局，和{}局，输{}局，胜率：{:.2f},不输率:{:.2f}"
                  .format(num, results[2], results[1], results[0], results[2]/num, (results[2]+results[1])/num))
        pass
