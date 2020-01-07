import time
import board
import displayio
from adafruit_progressbar import ProgressBar

# Make the display context
splash = displayio.Group(max_size=10)
board.DISPLAY.show(splash)

# Make a background color fill
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x0
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0,
                               pixel_shader=color_palette)
splash.append(bg_sprite)
##########################################################################

# set progress bar width and height relative to board's display
x = board.DISPLAY.width//5
y = board.DISPLAY.height//3

# Create a new progress_bar object at (x, y)
progress_bar = ProgressBar(x, y, 200, 30, 1.0)

# Append progress_bar to the splash group
splash.append(progress_bar)

progress_bar.progress = 0.75

progress_bar.progress = 0.5

progress_bar.progress = 1.0


"""
print("Progress: 0% -> 100%")
progress = 0.0
while progress <= 1.0:
    print("Progress: {}%".format(progress*100))
    progress_bar.progress = progress
    progress+=0.05
    time.sleep(0.03)
"""


"""
progress = 1.0
while progress > 0.0:
    print("Progress: {}%".format(progress*100))
    progress_bar.progress = progress
    progress-=0.1
    time.sleep(0.01)
"""

while True:
    pass

