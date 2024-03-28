import numpy as np
import matplotlib.pyplot as plt

def dynamic_rule(state, neighbors):
    # A dynamic rule based on the number of active neighbors
    active_neighbors = sum(neighbors)
    if state == 1 and active_neighbors in [1, 2]:
        return 1
    elif state == 0 and active_neighbors == 2:
        return 1
    else:
        return 0

class DynamicCellularAutomaton:
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
        history = [self.grid.copy()]
        for _ in range(steps):
            self.update()
            history.append(self.grid.copy())
        plt.imshow(history, cmap='binary', aspect='auto')
        plt.xlabel("Cell Index")
        plt.ylabel("Time Step")
        plt.title("Dynamic 1D Cellular Automaton")
        plt.show()

# Example of initializing the automaton with a specific initial state
initial_state = [0] * 25 + [1] + [0] * 24  # Single active cell in the middle

# Initialize and run the dynamic cellular automaton
automaton = DynamicCellularAutomaton(50, dynamic_rule, initial_state=initial_state)
automaton.animate(50)  # Visualize for 50 steps
