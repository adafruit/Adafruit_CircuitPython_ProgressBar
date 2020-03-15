# The MIT License (MIT)
#
# Copyright (c) 2020 Brent Rubell for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_progressbar`
================================================================================

Dynamic progress bar widget for CircuitPython displays


* Author(s): Brent Rubell

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

# pylint: disable=too-many-arguments, too-few-public-methods
class ProgressBar(displayio.TileGrid):
    """A dynamic progress bar widget.

    :param int x: The x-position of the top left corner.
    :param int y: The y-position of the top left corner.
    :param int width: The width of the progress bar.
    :param int height: The height of the progress bar.
    :param float progress: The percentage of the progress bar.
    :param bar_color: The color of the progress bar. Can be a hex
                                value for color.
    :param int outline_color: The outline of the progress bar. Can be a hex
                            value for color.
    :param int stroke: Used for the outline_color

    """

    # pylint: disable=invalid-name
    def __init__(
        self,
        x,
        y,
        width,
        height,
        progress=0.0,
        bar_color=0x00FF00,
        outline_color=0xFFFFFF,
        stroke=1,
    ):
        assert isinstance(progress, float), "Progress must be a floating point value."
        self._bitmap = displayio.Bitmap(width, height, 3)
        self._palette = displayio.Palette(3)
        self._palette[0] = 0x0
        self._palette[1] = outline_color
        self._palette[2] = bar_color

        self._width = width
        self._height = height

        self._progress_val = progress
        self.progress = self._progress_val

        # draw outline rectangle
        for _w in range(width):
            for line in range(stroke):
                self._bitmap[_w, line] = 1
                self._bitmap[_w, height - 1 - line] = 1
        for _h in range(height):
            for line in range(stroke):
                self._bitmap[line, _h] = 1
                self._bitmap[width - 1 - line, _h] = 1
        super().__init__(self._bitmap, pixel_shader=self._palette, x=x, y=y)

    @property
    def progress(self):
        """The percentage of the progress bar expressed as a
        floating point number.

        """
        return self._progress_val

    @progress.setter
    def progress(self, value):
        """Draws the progress bar

        :param float value: Progress bar value.
        """
        assert value <= 1.0, "Progress value may not be > 100%"
        assert isinstance(
            value, float
        ), "Progress value must be a floating point value."
        if self._progress_val > value:
            # uncolorize range from width*value+margin to width-margin
            for _w in range(int(value * self._width + 2), self._width - 2):
                for _h in range(2, self._height - 2):
                    self._bitmap[_w, _h] = 0
        else:
            # fully fill progress bar color
            for _w in range(2, self._width * value - 2):
                for _h in range(2, self._height - 2):
                    self._bitmap[_w, _h] = 2
        self._progress_val = value

    @property
    def fill(self):
        """The fill of the progress bar. Can be a hex value for a color or ``None`` for
        transparent.

        """
        return self._palette[0]

    @fill.setter
    def fill(self, color):
        """Sets the fill of the progress bar. Can be a hex value for a color or ``None`` for
        transparent.

        """
        if color is None:
            self._palette[2] = 0
            self._palette.make_transparent(0)
        else:
            self._palette[2] = color
            self._palette.make_opaque(0)
