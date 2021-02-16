# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import displayio
from adafruit_blinka import board
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_progressbar.progressbar import ProgressBar

display = PyGameDisplay(width=320, height=240, auto_refresh=False)
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# set progress bar width and height relative to board's display
width = 200
height = 120

# pylint: disable=no-member
x = board.DISPLAY.width // 2 - width // 2
y = board.DISPLAY.height // 3
# pylint: enable=no-member

# Create a new progress_bar object at (x, y)
progress_bar = ProgressBar(x, y, width, height, 1.0)

# Append progress_bar to the splash group
splash.append(progress_bar)

current_progress = 0.0
# Must check display.running in the main loop!
while display.running:
    display.refresh()
    # pass
