from simulation import Simulation
import os

if __name__ == "__main__":
    if os.path.exists("game_log.txt"):
        os.remove("game_log.txt")
    sim = Simulation(num_simulations=100, random_strategic="random")
    sim.run_simulation()
    sim.display_results()
