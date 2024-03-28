import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class CellularAutomaton:
    def __init__(self, rows, cols, rule_func):
        """
        Initializes the cellular automaton
        :param rows: Number of rows in the grid
        :param cols: Number of columns in the grid
        :param rule_func: A function that defines the rule of the automaton
        """
        self.grid = np.random.choice([0, 1], size=(rows, cols))
        self.rule_func = rule_func

    def update(self):
        """
        Updates the grid based on the rule function
        """
        new_grid = self.grid.copy()
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
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
        rows, cols = self.grid.shape
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r = (row + i) % rows
                c = (col + j) % cols
                neighbors.append(self.grid[r, c])
        return neighbors

    def animate(self, steps, interval=100):
        """
        Animates the evolution of the cellular automaton
        :param steps: Number of steps to animate
        :param interval: Time interval between frames in milliseconds
        """
        fig, ax = plt.subplots()
        img = ax.imshow(self.grid, interpolation='nearest')

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
