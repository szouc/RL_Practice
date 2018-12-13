from Player import Player
import math
from utils import get_dict, set_dict, epsilon_greedy_policy


class MC_Player(Player):
    def __init__(self, name="", A=None, display=False):
        super(MC_Player, self).__init__(name, A, display)
        self.Q = {}   # 某一状态行为对的价值，策略迭代时使用
        self.Nsa = {}  # Nsa的计数：某一状态行为对出现的次数
        self.total_learning_times = 0
        self.policy = self.greedy_policy
        self.learning_method = self.learn_Q

    def learn_Q(self, episode, r):  # 从状态序列来学习Q值
        '''从Episode学习
        '''
        # for episode, r in episodes:
        for s, a in episode:
            nsa = get_dict(self.Nsa, s, a)
            set_dict(self.Nsa, nsa+1, s, a)
            q = get_dict(self.Q, s, a)
            set_dict(self.Q, q+(r-q)/(nsa+1), s, a)
        self.total_learning_times += 1

    def reset_memory(self):
        '''忘记既往学习经历
        '''
        self.Q.clear()
        self.Nsa.clear()
        self.total_learning_times = 0

    def greedy_policy(self, dealer, epsilon=None):
        player_points, _ = self.get_points()
        if player_points >= 21:
            return self.A[1]
        if player_points < 12:
            return self.A[0]
        else:
            A, Q = self.A, self.Q
            s = self.get_state_name(dealer)
            if epsilon is None:
                #epsilon = 1.0/(self.total_learning_times+1)
                #epsilon = 1.0/(1 + math.sqrt(1 + player.total_learning_times))
                epsilon = 1.0 / \
                    (1 + 4 * math.log10(1+self.total_learning_times))
            return epsilon_greedy_policy(A, s, Q, epsilon)
