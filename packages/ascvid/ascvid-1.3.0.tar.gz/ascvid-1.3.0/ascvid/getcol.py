import colorama
from math import sqrt
import colorsys
colorama.init()
#### Please note that these colors might display differently on other terminals
_COLORS = {
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
COLORS = {colorsys.rgb_to_hsv(*k):v for k,v in _COLORS.items()}
def calc_dist(col1,col2):
    return 2*abs(col1[0] - col2[0])+ abs(col1[1]-col2[1])+ abs(col1[2]-col2[2])
def closest_color(color):
    color=colorsys.rgb_to_hsv(*color)
    min_d=min(COLORS,key=lambda d:calc_dist(color,d))
    return COLORS[min_d]
    
