import random
import numpy as np
import matplotlib.pyplot as plt

from cribbage import CribbageGame
from players import PlayerA, PlayerB


# for the game simulation

class Simulation:
    def __init__(self, num_simulations, random_strategic):
        self.num_simulations = num_simulations
        self.random_strategic = random_strategic
        self.results = {
            "Player 1 Wins": 0,
            "Player 2 Wins": 0,
            "Scores": []
        }

    def run_simulation(self):
        for n in range(self.num_simulations):
            if random.randint(0, 1) == 1:   # 0 means the player does not have crib
                game = CribbageGame(PlayerB(None), PlayerB([]))
                if self.random_strategic == "random":
                    game = CribbageGame(PlayerA(None), PlayerB([]))
            else:
                game = CribbageGame(PlayerB([]), PlayerB(None))
                if self.random_strategic == "random":
                    game = CribbageGame(PlayerA([]), PlayerB(None))

            game.start_game()
            self.get_results(game)

    def get_results(self, game):
        player1_score, player2_score = game.get_scores()
        if player1_score > player2_score:
            self.results["Player 1 Wins"] += 1
        else:
            self.results["Player 2 Wins"] += 1

        self.results["Scores"].append((player1_score, player2_score))

    def display_results(self):
        print("==============CRIBBAGE SIMULATION==============")
        if self.random_strategic == "random":
            print("Player 1 = Random   |   Player 2 = Strategic\n\n")
        else:
            print("Player 1 = Strategic   |   Player 2 = Strategic")
        print("Player 1 wins:" + str(self.results["Player 1 Wins"]))
        print("Player 2 wins:" + str(self.results["Player 2 Wins"]))

        p1_scores = [score[0] for score in self.results['Scores']]
        p2_scores = [score[1] for score in self.results['Scores']]
        p1_avg = np.average(p1_scores)
        p2_avg = np.average(p2_scores)

        print(f"Player 1 Average Score: {p1_avg}")
        print(f"Player 2 Average Score: {p2_avg}")

        self.plot_results(p1_avg, p2_avg)

    def plot_results(self, p1, p2):
        player1_scores = [score[0] for score in self.results["Scores"]]
        player2_scores = [score[1] for score in self.results["Scores"]]

        # Calculate margins (positive values mean Player 1 won by that margin, negative means Player 2 won)
        score_margins = [s1 - s2 for s1, s2 in zip(player1_scores, player2_scores)]

        plt.figure(figsize=(12, 6))  # Set figure size for better visibility

        plt.subplot(1, 2, 1)  # First subplot for individual scores
        plt.hist(player1_scores, bins=50, alpha=0.7, color='blue', label='Player 1 Scores')
        plt.hist(player2_scores, bins=50, alpha=0.7, color='red', label='Player 2 Scores')
        plt.xlabel('Scores')
        plt.ylabel('Frequency')
        plt.title('Score Distribution for Players')
        plt.legend(loc='upper right')

        plt.subplot(1, 2, 2)  # Second subplot for score margins
        plt.hist(score_margins, bins=50, alpha=0.7, color='green', label='Score Margins')
        plt.xlabel('Score Margin (Player 1 - Player 2)')
        plt.ylabel('Frequency')
        plt.title('Score Margin Distribution')
        plt.legend(loc='upper right')

        plt.suptitle(f"Player 1 Average = {p1}, Player 2 Average = {p2}", fontsize=14)
        plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make room for the main title
        plt.show()



