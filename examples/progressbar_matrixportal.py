# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Source: https://github.com/ajs256/matrixportal-weather-display

# ############## IMPORTS ###############

# HARDWARE
import time
import board

# DISPLAY
import displayio  # Main display library
import framebufferio  # For showing things on the display
import rgbmatrix  # For talking to matrices specifically

# CONTROLS

from adafruit_progressbar.progressbar import ProgressBar

# ############## DISPLAY SETUP ###############

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

print("Setting up RGB matrix")

# This next call creates the RGB Matrix object itself. It has the given width
# and height.
#
# These lines are for the Matrix Portal. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=32,
    bit_depth=3,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2,
    ],
    addr_pins=[board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE,
)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix)

print("Adding display group")
group = displayio.Group(max_size=5)  # Create a group to hold all our labels
display.show(group)

print("Creating progress bar and adding to group")
progress_bar = ProgressBar(2, 8, 40, 14, 0.6)

group.insert(0, progress_bar)

progress_bar_value = 0.0
progress_bar_incr = 3.0

while True:
    if progress_bar_value > 100:
        progress_bar_value = 100
        progress_bar_incr *= -1

    if progress_bar_value < 0:
        progress_bar_value = 0
        progress_bar_incr *= -1

    progress_bar.progress = progress_bar_value / 100
    progress_bar_value += progress_bar_incr
    time.sleep(0.5)
