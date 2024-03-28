import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class CellularAutomaton:
    def __init__(self, rows, cols, rule_func, initial_state=None):
        """
        Initializes the cellular automaton
        :param rows: Number of rows in the grid
        :param cols: Number of columns in the grid
        :param rule_func: A function that defines the rule of the automaton
        :param initial_state: Initial state of the grid (optional)
        """
        self.rows = rows
        self.cols = cols
        if initial_state is None:
            self.grid = np.random.choice([0, 1], size=(rows, cols))
        else:
            self.grid = np.array(initial_state)
        self.rule_func = rule_func

    def update(self):
        """
        Updates the grid based on the rule function
        """
        new_grid = self.grid.copy()
        for i in range(self.rows):
            for j in range(self.cols):
                state = self.grid[i, j]
                neighbors = self.get_neighbors(i, j)
                new_grid[i, j] = self.rule_func(state, neighbors)
        self.grid = new_grid

    def get_neighbors(self, row, col):
        """
        Returns the states of the neighbors of a cell
        :param row: Row of the cell
        :param col: Column of the cell
        :return: A list of the states of the neighbors
        """
        neighbors = self.grid[max(row-1, 0):min(row+2, self.rows),
                              max(col-1, 0):min(col+2, self.cols)].flatten()
        # Exclude the cell itself
        return np.delete(neighbors, len(neighbors)//2)

    def animate(self, steps, interval=100):
        """
        Animates the evolution of the cellular automaton
        :param steps: Number of steps to animate
        :param interval: Time interval between frames in milliseconds
        """
        fig, ax = plt.subplots()
        img = ax.imshow(self.grid, interpolation='nearest', cmap='viridis')

        def update_frame(*args):
            self.update()
            img.set_data(self.grid)
            return img,

        ani = FuncAnimation(fig, update_frame, frames=steps, interval=interval, blit=True)
        plt.show()

# Example rule function for Conway's Game of Life
def conways_rule(state, neighbors):
    alive_neighbors = sum(neighbors)
    if state == 1 and alive_neighbors < 2:
        return 0
    elif state == 1 and alive_neighbors > 3:
        return 0
    elif state == 0 and alive_neighbors == 3:
        return 1
    else:
        return state

# Initialize and run the cellular automaton
automaton = CellularAutomaton(50, 50, conways_rule)
automaton.animate(100)
