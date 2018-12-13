from utils import set_dict, get_dict


class Evaluate():

    def __init__(self, arena, player, dealer, num):
        self.arena = arena
        self.player = player
        self.dealer = dealer
        self.num = num
        self.V = {}
        self.Ns = {}

    def policy_evaluate(self):
        self.arena.play_games(self.dealer, self.player, self.num)
        for episode, r in self.arena.episodes:
            for s, a in episode:
                ns = get_dict(self.Ns, s)
                v = get_dict(self.V, s)
                set_dict(self.Ns, ns+1, s)
                set_dict(self.V, v+(r-v)/(ns+1), s)
