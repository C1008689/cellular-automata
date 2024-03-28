import numpy as np
import matplotlib.pyplot as plt

def advanced_rule(state, neighbors):
    # A more complex rule: A cell toggles its state if exactly one neighbor is in state 1
    return 1 - state if sum(neighbors) == 1 else state

class AdvancedCellularAutomaton:
    def __init__(self, size, rule_func, initial_state=None):
        self.size = size
        self.rule_func = rule_func
        if initial_state is not None:
            self.grid = np.array(initial_state)
        else:
            self.grid = np.random.choice([0, 1], size=size)

    def update(self):
        new_grid = np.copy(self.grid)
        for i in range(1, self.size - 1):
            neighbors = [self.grid[i-1], self.grid[i+1]]
            new_grid[i] = self.rule_func(self.grid[i], neighbors)
        self.grid = new_grid

    def animate(self, steps):
        plt.figure()
        for step in range(steps):
            if step == 0:
                plt.imshow([self.grid], cmap='binary', aspect='auto')
            else:
                self.update()
                plt.imshow([self.grid], cmap='binary', aspect='auto', extent=[0, self.size, step, step+1])
        plt.xlabel("Cell Index")
        plt.ylabel("Time Step")
        plt.title("Advanced 1D Cellular Automaton")
        plt.show()

# Example of initializing the automaton with a specific initial state
initial_state = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0,
                 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
                 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# Initialize and run the advanced cellular automaton
automaton = AdvancedCellularAutomaton(50, advanced_rule, initial_state=initial_state)
automaton.animate(30)  # Visualize for 30 steps
