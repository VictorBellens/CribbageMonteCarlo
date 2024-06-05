from simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(num_simulations=1000, random_strategic="str")
    sim.run_simulation()
    sim.display_results()
