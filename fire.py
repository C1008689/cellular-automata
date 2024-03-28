import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib import animation
from matplotlib import colors
from scipy.signal import convolve2d

# Constants for the cell states
EMPTY, TREE, FIRE = 0, 1, 2

# Function to initialize the forest grid
def initialize_grid(nx, ny, forest_fraction):
    X = np.zeros((ny, nx), dtype=int)
    X[1:ny-1, 1:nx-1] = np.random.choice([EMPTY, TREE], size=(ny-2, nx-2), p=[1-forest_fraction, forest_fraction])
    return X

# Optimized iteration function using convolution for neighbor counting
def iterate_with_wind(X, p, f, wind_speed):
    kernel = np.ones((3, 3), dtype=int)
    kernel[1, 1] = 0

    tree_neighbors = convolve2d(X == TREE, kernel, mode='same', boundary='fill', fillvalue=EMPTY)
    fire_neighbors = convolve2d(X == FIRE, kernel, mode='same', boundary='fill', fillvalue=EMPTY)

    grow_trees = (X == EMPTY) & (np.random.rand(*X.shape) < p)
    catch_fire = (X == TREE) & ((fire_neighbors > 0) | (np.random.rand(*X.shape) < f))

    # Wind effect: Increase the chance of catching fire based on wind speed
    # This example assumes an eastward wind, modifying for other directions is similar
    if wind_speed > 0:
        east_wind_effect = np.roll(X == FIRE, -wind_speed, axis=1) & (X == TREE)
        catch_fire |= east_wind_effect

    X1 = X.copy()
    X1[grow_trees] = TREE
    X1[catch_fire] = FIRE
    X1[X == FIRE] = EMPTY

    return X1

# Visualization setup
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.4)

colors_list = [(0.2, 0, 0), (0, 0.5, 0), (1, 0, 0), 'orange']
cmap = colors.ListedColormap(colors_list)
norm = colors.BoundaryNorm([0, 1, 2, 3], cmap.N)

# Sliders for adjusting probabilities and wind speed
axcolor = 'lightgoldenrodyellow'
ax_p = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_f = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_wind = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)

p_slider = Slider(ax_p, 'Growth Prob', 0.01, 0.1, valinit=0.05)
f_slider = Slider(ax_f, 'Fire Prob', 0.0001, 0.001, valinit=0.0001)
wind_slider = Slider(ax_wind, 'Wind Speed', 0, 5, valinit=0, valstep=1)

# Prompt for grid size initialization
scale_factor = float(input("Enter scale factor (e.g., 1 for 100x100, 2 for 200x200): "))
nx, ny = int(100 * scale_factor), int(100 * scale_factor)
forest_fraction = 0.2
forest = initialize_grid(nx, ny, forest_fraction)
im = ax.imshow(forest, cmap=cmap, norm=norm)

# Update function for the animation
def update(frame):
    global forest, p, f, wind_speed
    p, f = p_slider.val, f_slider.val
    wind_speed = int(wind_slider.val)
    forest = iterate_with_wind(forest, p, f, wind_speed)
    im.set_array(forest)
    return [im]

ani = animation.FuncAnimation(fig, update, frames=200, blit=True, interval=100)
plt.show()
