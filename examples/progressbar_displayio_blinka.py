#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_progressbar.progressbar import ProgressBar
from adafruit_progressbar.verticalprogressbar import VerticalProgressBar
from adafruit_progressbar.horizontalprogressbar import HorizontalProgressBar

display = PyGameDisplay(width=320, height=240, auto_refresh=False)
splash = displayio.Group(max_size=10)
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x2266AA  # Teal-ish-kinda

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

progress_bar = ProgressBar(
    width=180,
    height=40,
    x=10,
    y=20,
    progress=0.0,
    bar_color=0x1100FF,
    outline_color=0xFF0000,
)
splash.append(progress_bar)
horizontal_bar = HorizontalProgressBar(
    (10, 90),
    (180, 40),
    value=-10,
    min_value=(-40),
    max_value=120,
    fill_color=0x00FF00,
    outline_color=0x0000FF,
    bar_color=0xFF0000,
)
splash.append(horizontal_bar)
vertical_bar = VerticalProgressBar((200, 30), (32, 180))
splash.append(vertical_bar)

# Must check display.running in the main loop!
while display.running and vertical_bar.value < 100:
    # progress_bar.progress += 0.01
    vertical_bar.value += 1
    # horizontal_bar.value += 1
    display.refresh()
    time.sleep(0.5)