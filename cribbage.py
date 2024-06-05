import itertools
from utils import Deck


class CribbageGame:
    def __init__(self, player_1, player_2):
        self.player1 = player_1
        self.player2 = player_2

        self.deck = Deck()
        self.starter_card = None
        self.crib = []

        self.current_player = self.player2
        if self.player1.crib is None:
            self.current_player = self.player1

    def start_game(self):
        while self.player1.score <= 121 and self.player2.score <= 121:
            self.deck.shuffle()
            self.deal_cards()
            self.choose_starter_card()
            self.play_phase()
            self.counting_phase()

    def deal_cards(self):
        if self.deck.getLength() < 12:  # If not enough cards to deal another round
            self.deck.reset()  # Assuming there's a reset method that repopulates and shuffles the deck
            self.deck.shuffle()
        self.player1.drawCards(self.deck, 6)
        self.player2.drawCards(self.deck, 6)

    def choose_starter_card(self):
        self.starter_card = self.deck.getCut()

    def counting_phase(self):
        self.player1.score += self.score_hand(self.player1.original_hand, self.starter_card)
        self.player2.score += self.score_hand(self.player2.original_hand, self.starter_card)

        if self.player1.crib is not None:
            self.player1.score += self.score_hand(self.player1.crib, self.starter_card)
        else:
            self.player2.score += self.score_hand(self.player2.crib, self.starter_card)

    def score_hand(self, hand, starter_card):
        total_score = 0
        all_cards = hand + [starter_card]

        total_score += self.findPairs(all_cards)
        total_score += self.findRuns(all_cards)
        total_score += self.findFifteens(all_cards)
        total_score += self.scoreFlush(hand, starter_card)
        total_score += self.scoreNobs(hand, starter_card)

        return total_score

    def findPairs(self, cards):
        count = 0
        values = [card.value for card in cards]
        for value in set(values):
            count += values.count(value) * (values.count(value) - 1) // 2
        return 2 * count

    def findRuns(self, cards):
        # To check for all possible runs, sort the cards
        score = 0
        sorted_cards = sorted(cards, key=lambda x: x.value)
        length = len(sorted_cards)
        for start in range(length):
            run_length = 1
            for end in range(start + 1, length):
                if sorted_cards[end].value == sorted_cards[end - 1].value + 1:
                    run_length += 1
                elif sorted_cards[end].value != sorted_cards[end - 1].value:
                    break
            if run_length >= 3:
                score += run_length
        return score

    def findFifteens(self, cards):
        score = 0
        for combo in itertools.combinations(cards, 2):
            if sum(card.value for card in combo) == 15:
                score += 2
        return score

    def scoreFlush(self, hand, starter_card):
        if all(card.suit == hand[0].suit for card in hand):
            return 5 if all(card.suit == starter_card.suit for card in hand + [starter_card]) else 4
        return 0

    def scoreNobs(self, hand, starter_card):
        return 1 if any(card.rank == 'Jack' and card.suit == starter_card.suit for card in hand) else 0

    def play_phase(self):
        history = []  # Tracks all cards played in the current round
        running_total = 0  # Sum of values of cards played in the current round
        last_player = None  # Tracks who played the last card

        while any(self.player1.hand) or any(self.player2.hand):
            no_cards_played = True  # Tracks if no cards are played in a loop, indicating a 'go' situation

            for player in [self.current_player, self.get_opponent(self.current_player)]:
                if player.hand:
                    card_played = player.playCard(history)
                    if card_played:
                        no_cards_played = False
                        running_total += card_played.value
                        history.append(card_played)
                        last_player = player

                        # Check for scoring moves
                        self.score_play(history, running_total)

                        if running_total == 31:
                            player.updateScore(2)  # Score for hitting 31 exactly
                            running_total = 0
                            history.clear()  # Reset for the next sequence
                        elif running_total > 31:
                            running_total -= card_played.value  # Remove the last card's value
                            history.pop()  # Remove the last card played
                            continue  # Skip to next player since this card cannot be played

                    else:
                        # If player cannot play, check if the opponent can play
                        opponent = self.get_opponent(player)
                        if not opponent.canPlayCard(history, 31 - running_total):
                            if last_player and no_cards_played:
                                last_player.updateScore(1)  # Score for a "go"
                            running_total = 0
                            history.clear()
                            break  # Exit the loop if no cards can be played by either

            self.current_player = self.get_opponent(self.current_player)  # Switch turns

    def score_play(self, history, running_total):
        if len(history) < 2:
            return  # Not enough cards to score any points other than 15 or 31, which are handled elsewhere

        last_card = history[-1]
        # Scoring for pairs, triples, and quadruples
        if len(history) >= 2:
            pair_count = sum(1 for card in history[-2:] if card.value == last_card.value)
            if pair_count == 2:
                self.current_player.updateScore(2)  # Pair
            elif pair_count == 3:
                self.current_player.updateScore(6)  # Triple
            elif pair_count == 4:
                self.current_player.updateScore(12)  # Quadruple

        # Scoring for runs
        for length in range(3, len(history) + 1):
            last_n_cards = history[-length:]
            if self.isRun(last_n_cards):
                self.current_player.updateScore(length)  # Score is the length of the run

        # Check for fifteens
        if running_total == 15:
            self.current_player.updateScore(2)  # Score for reaching fifteen

    def isRun(self, cards):
        if len(cards) < 3:
            return False
        sorted_cards = sorted(cards, key=lambda x: x.value)
        return all(sorted_cards[i].value - sorted_cards[i - 1].value == 1 for i in range(1, len(sorted_cards)))

    def get_opponent(self, current_player):
        return self.player2 if current_player == self.player1 else self.player1

    def get_scores(self):
        return self.player1.score, self.player2.score
