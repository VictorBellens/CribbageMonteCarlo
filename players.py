
import random
import itertools

from utils import calculatePotentialScore, evaluateCardScore, defensiveScore

# PlayerA = RANDOM play style
# PlayerB = STRATEGIC play style


class PlayerA:
    def __init__(self, crib):
        # Game Logic
        self.hand = []  # 6
        self.original_hand = []    # 4
        self.crib = crib  # 2/4     list
        self.score = 0  # max 121

    def laysAway(self):
        layaway = [self.hand.pop(random.randint(0, len(self.hand) - 1)),
                   self.hand.pop(random.randint(0, len(self.hand) - 1))]
        self.original_hand = self.hand
        return layaway

    def playCard(self, history):
        return self.hand.pop(random.randint(0, len(self.hand) - 1)) if self.hand else None

    def canPlayCard(self, history, max_score):
        # Method to check if any card in hand can be played without exceeding the running total
        current_total = sum(card.value for card in history)
        return any(card.value + current_total <= max_score for card in self.hand)

    def drawCards(self, deck, num_cards):
        self.hand = [deck.getTop() for _ in range(num_cards)]

    def updateScore(self, points):
        self.score += points

    def getHand(self):
        hands = []
        for card in self.original_hand:
            hands.append((card.value, card.suit))
        return hands


class PlayerB(PlayerA):
    def __init__(self, crib):
        super().__init__(crib)

    def laysAway(self):
        sorted_hand = sorted(self.hand, key=lambda card: card.value)
        self.hand = sorted_hand
        self.original_hand = self.hand

        max_score = -1
        min_score = 99
        best_combination = None
        all_combinations = list(itertools.combinations(self.hand, 4))

        for combination in all_combinations:
            score = calculatePotentialScore(combination)
            if score > max_score:
                max_score = score
                best_combination = combination
            if score < min_score:
                worst_combination = combination

        if self.crib is not None:
            self.original_hand = list(best_combination)
            layaway = [card for card in self.hand if card not in best_combination]
            self.hand = self.original_hand
            return layaway
        else:
            return self.hand.pop(0), self.hand.pop(0)

            # if SIMULATION is bad, consider using "worst_combination"

    def playCard(self, history):
        current_total = sum(card.value for card in history) % 31
        valid_plays = [card for card in self.hand if card.value + current_total <= 31]

        if not valid_plays:
            return None  # No valid cards to play, say "Go"

        best_card = max(valid_plays,
                        key=lambda card: evaluateCardScore(card, current_total, history) - defensiveScore(
                            card, current_total, history))

        self.hand.remove(best_card)  # Remove the chosen card from hand
        return best_card

