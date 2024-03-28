import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ForestSimulation:
    EMPTY, TREE, BURNING = 0, 1, 2  # States

    def __init__(self, rows, cols, growth_prob, fire_prob):
        self.rows = rows
        self.cols = cols
        self.grid = np.random.choice([self.EMPTY, self.TREE], 
                                     size=(rows, cols), 
                                     p=[1-growth_prob, growth_prob])
        self.growth_prob = growth_prob
        self.fire_prob = fire_prob

    def update(self):
        new_grid = np.copy(self.grid)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == self.TREE:
                    if self.is_burning_neighbor(i, j):
                        new_grid[i, j] = self.BURNING
                elif self.grid[i, j] == self.BURNING:
                    new_grid[i, j] = self.EMPTY
                elif self.grid[i, j] == self.EMPTY:
                    if np.random.rand() < self.growth_prob:
                        new_grid[i, j] = self.TREE
                
                # Randomly start fires
                if self.grid[i, j] == self.TREE and np.random.rand() < self.fire_prob:
                    new_grid[i, j] = self.BURNING

        self.grid = new_grid

    def is_burning_neighbor(self, row, col):
        for i in range(max(row-1, 0), min(row+2, self.rows)):
            for j in range(max(col-1, 0), min(col+2, self.cols)):
                if (i != row or j != col) and self.grid[i, j] == self.BURNING:
                    return True
        return False

    def animate(self, steps, interval=100):
        fig, ax = plt.subplots()
        img = ax.imshow(self.grid, cmap='Greens', interpolation='nearest')

        def update_frame(*args):
            self.update()
            img.set_data(self.grid)
            return img,

        ani = FuncAnimation(fig, update_frame, frames=steps, interval=interval, blit=True)
        plt.show()

# Initialize and run the forest simulation
forest_sim = ForestSimulation(50, 50, growth_prob=0.01, fire_prob=0.001)
forest_sim.animate(200)
