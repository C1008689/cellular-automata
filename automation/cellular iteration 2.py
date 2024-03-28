import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation

class CellularAutomaton:
    def __init__(self, rows, cols, rule_func, initial_state=None, cmap='viridis'):
        """
        Initializes the cellular automaton
        :param rows: Number of rows in the grid
        :param cols: Number of columns in the grid
        :param rule_func: A function that defines the rule of the automaton
        :param initial_state: Initial state of the grid (optional)
        :param cmap: Color map for visualization
        """
        self.rows = rows
        self.cols = cols
        self.grid = np.random.choice([0, 1], size=(rows, cols)) if initial_state is None else np.array(initial_state)
        self.rule_func = rule_func
        self.cmap = cmap

    def update(self):
        new_grid = np.copy(self.grid)
        for i in range(self.rows):
            for j in range(self.cols):
                state = self.grid[i, j]
                neighbors = self.get_neighbors(i, j)
                new_grid[i, j] = self.rule_func(state, neighbors)
        self.grid = new_grid

    def get_neighbors(self, row, col):
        neighbors = self.grid[max(row-1, 0):min(row+2, self.rows),
                              max(col-1, 0):min(col+2, self.cols)].flatten()
        return np.delete(neighbors, len(neighbors)//2)

    def animate(self, steps, interval=100):
        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.1, bottom=0.25)
        img = ax.imshow(self.grid, interpolation='nearest', cmap=self.cmap)

        axcolor = 'lightgoldenrodyellow'
        ax_scale = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
        scale_slider = Slider(ax_scale, 'Scale', 1, 10, valinit=1, valstep=1)

        def update_frame(*args):
            self.update()
            img.set_data(self.grid)
            img.set_cmap(self.cmap)
            return img,

        def update(val):
            scale_factor = scale_slider.val
            img.set_data(np.kron(self.grid, np.ones((scale_factor, scale_factor))))
            fig.canvas.draw_idle()

        scale_slider.on_changed(update)
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
automaton = CellularAutomaton(50, 50, conways_rule, cmap='plasma')
automaton.animate(100)
