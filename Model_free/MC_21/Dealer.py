from Gamer import Gamer


class Dealer(Gamer):

    def __init__(self, name="", A=None, display=False):
        super(Dealer, self).__init__(name, A, display)
        self.role = 'Dealer'
        self.policy = self.dealer_policy

    def first_card_value(self):
        if self.cards is None or len(self.cards) == 0:
            return 0
        return self._value_of(self.cards[0])

    def dealer_policy(self, Dealer=None):
        action = ""
        dealer_points, _ = self.get_points()
        if dealer_points >= 17:
            action = self.A[1]
        else:
            action = self.A[0]
        return action

    def cards_info(self):
        super().cards_info(self.role)
