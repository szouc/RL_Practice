from Gamer import Gamer
from utils import str_key


class Player(Gamer):

    def __init__(self, name="", A=None, display=False):
        super(Player, self).__init__(name, A, display)
        self.policy = self.naive_policy
        self.role = 'Player'

    def get_state(self, dealer):
        dealer_first_card_value = dealer.first_card_value()
        player_points, useable_ace = self.get_points()
        return dealer_first_card_value, player_points, useable_ace

    def get_state_name(self, dealer):
        return str_key(self.get_state(dealer))

    def naive_policy(self, dealer=None):
        player_points, _ = self.get_points()
        if player_points < 20:
            action = self.A[0]
        else:
            action = self.A[1]
        return action

    def cards_info(self):
        super().cards_info(self.role)
