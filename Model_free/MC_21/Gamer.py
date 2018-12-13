class Gamer():

    def __init__(self, name="", A=None, display=False):
        self.name = name
        self.cards = []
        self.display = display
        self.policy = None
        self.learning_method = None
        self.A = A

    def __str__(self):
        return self.name

    def _value_of(self, card):
        try:
            v = int(card)
        except:
            if card == 'A':
                v = 1
            elif card in ['J', 'Q', 'K']:
                v = 10
            else:
                v = 0
        finally:
            return v

    def get_points(self):
        num_of_useable_ace = 0
        total_point = 0
        cards = self.cards
        if cards is None:
            return 0, False
        for card in cards:
            v = self._value_of(card)
            if v == 1:
                num_of_useable_ace += 1
                v = 11
            total_point += v
        while total_point > 21 and num_of_useable_ace > 0:
            total_point -= 10
            num_of_useable_ace -= 1
        return total_point, bool(num_of_useable_ace)

    def receive(self, cards=[]):
        cards = list(cards)
        for card in cards:
            self.cards.append(card)

    def discharge_cards(self):
        self.cards.clear()

    def _info(self, msg):
        if self.display:
            print(msg, end="")

    def cards_info(self, role):
        self._info("{}{}: Now, the cards are: {}\n".format(
            role, self, self.cards))
