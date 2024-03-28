import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ForestSimulation:
    EMPTY, TREE, BURNING = 0, 1, 2  # States
    BURN_DURATION = 3  # Number of steps a tree remains burning

    def __init__(self, rows, cols, growth_prob, fire_prob, fire_jump_prob):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.burn_timer = np.zeros((rows, cols), dtype=int)  # Timer for burning trees
        self.growth_prob = growth_prob
        self.fire_prob = fire_prob
        self.fire_jump_prob = fire_jump_prob
        self.initialize_forest()

    def initialize_forest(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i, j] = np.random.choice([self.EMPTY, self.TREE], p=[1-self.growth_prob, self.growth_prob])

    def update(self):
        new_grid = np.copy(self.grid)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == self.TREE:
                    if self.is_burning_neighbor(i, j) or (np.random.rand() < self.fire_jump_prob and self.has_tree_neighbor(i, j)):
                        new_grid[i, j] = self.BURNING
                        self.burn_timer[i, j] = self.BURN_DURATION
                elif self.grid[i, j] == self.BURNING:
                    if self.burn_timer[i, j] > 0:
                        self.burn_timer[i, j] -= 1
                    else:
                        new_grid[i, j] = self.EMPTY
                elif self.grid[i, j] == self.EMPTY:
                    if np.random.rand() < self.growth_prob * self.tree_neighbor_count(i, j) / 8:
                        new_grid[i, j] = self.TREE
                
                # Randomly start fires
                if self.grid[i, j] == self.TREE and np.random.rand() < self.fire_prob:
                    new_grid[i, j] = self.BURNING
                    self.burn_timer[i, j] = self.BURN_DURATION

        self.grid = new_grid

    def tree_neighbor_count(self, row, col):
        count = 0
        for i in range(max(row-1, 0), min(row+2, self.rows)):
            for j in range(max(col-1, 0), min(col+2, self.cols)):
                if self.grid[i, j] == self.TREE:
                    count += 1
        return count

    def is_burning_neighbor(self, row, col):
        for i in range(max(row-1, 0), min(row+2, self.rows)):
            for j in range(max(col-1, 0), min(col+2, self.cols)):
                if (i != row or j != col) and self.grid[i, j] == self.BURNING:
                    return True
        return False

    def has_tree_neighbor(self, row, col):
        return self.tree_neighbor_count(row, col) > 0

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
forest_sim = ForestSimulation(50, 50, growth_prob=0.02, fire_prob=0.001, fire_jump_prob=0.0005)
forest_sim.animate(200)

