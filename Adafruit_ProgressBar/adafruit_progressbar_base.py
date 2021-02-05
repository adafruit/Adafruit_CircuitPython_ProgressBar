# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_progressbar`
================================================================================

Dynamic progress bar widget for CircuitPython displays


* Author(s): Brent Rubell and Hugo Dahl

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/brentru/Adafruit_CircuitPython_ProgressBar.git"


class ProgressBarBase(displayio.TileGrid):
    def __init__(
        self,
        position: (int, int),
        size: (int, int),
        start_value: float = 0.0,
        bar_color=0x00FF00,
        outline_color=0xFFFFFF,
        fill_color=0x000000,
    ):

        self._size = size
        self._position = position
        self._progress = start_value
        self._bitmap = displayio.Bitmap(self.width, self.height, 3)
        self._palette = displayio.Palette(3)
        self._palette[0] = fill_color
        self._palette[1] = outline_color
        self._palette[2] = bar_color

        super(ProgressBarBase, self).__init__(
            self._bitmap,
            pixel_shader=self._palette,
            x=self._position[0],
            y=self._position[1],
        )

    _bitmap: displayio.Bitmap  # The bitmap used for the bar/value
    _position: (int, int)  # The (x,y) coordinates of the top-left corner
    _size: (int, int)  # The dimensions of the progress bar
    _palette: displayio.Palette(3)  # The palette to be used
    _progress: float  # The value to represent, between 0.0 and 100.0

    @property.getter
    def width(self):
        return self._size[0]

    @property.getter
    def height(self):
        return self._size[1]

    @property.getter
    def x(self):
        return self._position[0]

    @property.getter
    def y(self):
        return self._position[1]

    @property
    def progress(self):
        return self._progress

    @property.setter
    def progress(self, value):
        self._progress = value
        self.render()

    def render(self):
        pass
