from surface_properties import Colour

BLACK = Colour((0,0,0), 'rgb')

GREY = Colour((125,125,125), 'rgb')
RED = Colour((255,0,0), 'rgb')
GREEN = Colour((0,255,0), 'rgb')
BLUE = Colour((0,0,255), 'rgb')

YELLOW = RED + GREEN
CYAN = GREEN + BLUE
MAGENTA = BLUE + RED
WHITE = RED + GREEN + BLUE
GRAY = WHITE * 0.5