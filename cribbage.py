from utils import isRun, score_hand
from cards import Deck

class CribbageGame:
    def __init__(self, player_1, player_2):
        self.player1 = player_1
        self.player2 = player_2

        self.deck = Deck()
        self.starter_card = None
        self.crib = []
        self.rounds = 0

        self.current_player = self.player2
        if self.player1.crib is None:
            self.current_player = self.player1

    def start_game(self):
        with open('game_log.txt', 'a') as file:  # Open a file in append mode
            file.write("Points scored during Pegging are not considered.\n\n")
            while self.player1.score <= 121 and self.player2.score <= 121:
                self.rounds += 1
                self.deck.shuffle()
                self.deal_cards()

                # Lay away cards and determine crib ownership
                p1_crib = self.player1.laysAway()
                p2_crib = self.player2.laysAway()

                crib_hand = [p1_crib[0], p1_crib[1], p2_crib[0], p2_crib[1]]

                if self.player1.crib is None:
                    self.player1.crib = crib_hand
                    self.player2.crib = None
                    crib_owner = self.player1
                else:
                    self.player2.crib = crib_hand
                    self.player1.crib = None
                    crib_owner = self.player2

                self.choose_starter_card()

                # Log the hands of each player and the starter card
                file.write(f"Player 1 Hand: {self.player1.getHand()}\n")
                file.write(f"Player 2 Hand: {self.player2.getHand()}\n")
                file.write(f"Starter Card: {self.starter_card.value, self.starter_card.suit}\n")

                self.play_phase()
                self.counting_phase()

                # Log the crib
                file.write(f"Crib Hand: {[(card.value, card.suit) for card in crib_hand]}\n")
                file.write(f"Crib Owner: {'Player 1' if crib_owner == self.player1 else 'Player 2'}\n")

                # Score the crib
                crib_score = score_hand(crib_hand, self.starter_card)
                crib_owner.updateScore(crib_score)

                # Log the scores after counting
                file.write(f"Scores - Player 1: {self.player1.score}, Player 2: {self.player2.score}\n")
                file.write("-------------------------------------------------\n")

    def crib_hand(self):
        if self.player1.crib is not None:
            return self.player1.crib
        else:
            return self.player2.crib

    def deal_cards(self):
        if self.deck.getLength() < 12:  # If not enough cards to deal another round
            self.deck.reset()  # Assuming there's a reset method that repopulates and shuffles the deck
            self.deck.shuffle()
        self.player1.drawCards(self.deck, 6)
        self.player2.drawCards(self.deck, 6)

    def choose_starter_card(self):
        self.starter_card = self.deck.getCut()

    def counting_phase(self):
        self.player1.score += score_hand(self.player1.original_hand, self.starter_card)
        self.player2.score += score_hand(self.player2.original_hand, self.starter_card)

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

                        if running_total == 15:
                            player.updateScore(2)
                        elif running_total == 31:
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
            if isRun(last_n_cards):
                self.current_player.updateScore(length)  # Score is the length of the run

    def get_opponent(self, current_player):
        return self.player2 if current_player == self.player1 else self.player1

    def get_scores(self):
        return self.player1.score, self.player2.score, self.rounds
