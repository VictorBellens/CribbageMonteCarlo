
import random
import itertools

# PlayerA = RANDOM
# PlayerB = STRATEGIC


class PlayerA:
    def __init__(self, crib):
        # Game Logic
        self.hand = []  # 6
        self.original_hand = []    # 4
        self.crib = crib  # 2/4     list
        self.score = 0  # max 121

    def laysAway(self):
        layaway = [self.hand.pop(random.randint(0, len(self.hand))), self.hand.pop(random.randint(0, len(self.hand)))]
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


class PlayerB(PlayerA):
    def __init__(self, crib):
        super().__init__(crib)

    def laysAway(self):
        self.hand.sort()
        max_score = -1
        min_score = 99
        best_combination = None
        all_combinations = list(itertools.combinations(self.hand, 4))

        for combination in all_combinations:
            score = self.calculatePotentialScore(combination)
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
                        key=lambda card: self.evaluateCardScore(card, current_total, history) - self.defensiveScore(
                            card, current_total, history))

        self.hand.remove(best_card)  # Remove the chosen card from hand
        return best_card

    def defensiveScore(self, card, current_total, history):
        risky_score = 0
        new_total = current_total + card.value

        if new_total == 15 or new_total == 31:
            risky_score += 2

        if any(h_card.value == card.value for h_card in history):
            risky_score += 2

        potential_run_completion = [card.value - 1, card.value + 1]
        for potential_value in potential_run_completion:
            if any(h_card.value == potential_value for h_card in history):
                risky_score += 1

        return -risky_score

    def evaluateCardScore(self, card, current_total, history):
        potential_score = 0

        # Calculate new total
        new_total = current_total + card.value

        # Score for reaching 15 or 31
        if new_total == 15 or new_total == 31:
            potential_score += 2

        # Evaluating potential for pairs, triples, and quadruples
        same_value_count = sum(1 for h_card in history if h_card.value == card.value)
        if same_value_count == 1:
            potential_score += 2  # Pair
        elif same_value_count == 2:
            potential_score += 6  # Triple
        elif same_value_count == 3:
            potential_score += 12  # Quadruple

        # Evaluating runs, considering the current card with the history
        all_cards = history + [card]
        for length in range(3, len(all_cards) + 1):  # Runs must be at least 3 cards long
            for subset in itertools.combinations(all_cards, length):
                if self.isRun(list(subset)):
                    potential_score += length  # Score equals the length of the run

        return potential_score

    def isRun(self, cards):
        if len(cards) < 3:
            return False
        cards_sorted = sorted(cards, key=lambda x: x.value)
        return all(cards_sorted[i].value - cards_sorted[i - 1].value == 1 for i in range(1, len(cards_sorted)))

    def findFifteens(self, cards):
        # Count combinations that sum to 15
        count = 0
        for num_cards in range(2, len(cards) + 1):
            for combo in itertools.combinations(cards, num_cards):
                if sum(card.value for card in combo) == 15:
                    count += 1
        return 2 * count  # Each 15 is 2 points

    def findPairs(self, cards):
        # Count pairs
        count = 0
        values = [card.value for card in cards]
        for value in set(values):
            count += values.count(value) * (values.count(value) - 1) // 2
        return 2 * count  # Pair is 2 points

    def findRuns(self, cards):
        # Check for runs (minimum length of 3)
        score = 0
        cards_sorted = sorted(cards, key=lambda x: x.value)
        for length in range(3, len(cards_sorted) + 1):
            for subset in itertools.combinations(cards_sorted, length):
                if all(subset[i].value - subset[i - 1].value == 1 for i in range(1, length)):
                    score += length  # score is length of run
        return score

    def calculatePotentialScore(self, cards):
        score = 0
        score += self.findFifteens(cards)
        score += self.findPairs(cards)
        score += self.findRuns(cards)
        return score

