import colorama
from math import sqrt
import numpy as np
colorama.init()
#### Please note that these colors might display differently on other terminals
COLORS = {
    (0, 0, 0): colorama.Fore.BLACK,
    (128, 0, 0): colorama.Fore.RED,
    (0, 128, 0): colorama.Fore.GREEN,
    (128, 128, 0): colorama.Fore.YELLOW,
    (0, 0, 128): colorama.Fore.BLUE,
    (128, 0, 128): colorama.Fore.MAGENTA,
    (0, 128, 128): colorama.Fore.CYAN,
    (192, 192, 192): colorama.Fore.WHITE,
    (128, 128, 128): colorama.Fore.LIGHTBLACK_EX,
    (255, 0, 0): colorama.Fore.LIGHTRED_EX,
    (0, 255, 0): colorama.Fore.LIGHTGREEN_EX,
    (255, 255, 0): colorama.Fore.LIGHTYELLOW_EX,
    (0, 255, 255): colorama.Fore.LIGHTCYAN_EX,
    (255, 0, 255): colorama.Fore.LIGHTMAGENTA_EX,
    (255, 255, 255): colorama.Fore.LIGHTWHITE_EX,

}
COLKEYS=list(COLORS.keys())
def closest_color(color):
    colors = np.array(COLKEYS)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return COLORS[tuple(smallest_distance.tolist()[0])]
