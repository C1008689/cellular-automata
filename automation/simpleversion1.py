import numpy as np
import matplotlib.pyplot as plt

def simple_rule(state, neighbors):
    # Simple rule: A cell becomes 1 if exactly one of its neighbors is 1
    return 1 if sum(neighbors) == 1 else 0

class SimpleCellularAutomaton:
    def __init__(self, size, rule_func):
        self.size = size
        self.grid = np.random.choice([0, 1], size=size)
        self.rule_func = rule_func

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
        plt.title("Simple 1D Cellular Automaton")
        plt.show()

# Initialize and run the simple cellular automaton
automaton = SimpleCellularAutomaton(50, simple_rule)
automaton.animate(30)
