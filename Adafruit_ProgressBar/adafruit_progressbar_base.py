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
    """The base class for dynamic progress bar widgets.

    :param (int, int) position: The coordinates (x, y) of the top left corner
    :param (int, int) size: The size (width, height) of the progress bar
    :param flaot start_value: The beginning value of the progress bar. This value
                              is displayed when the progress bar is first visible,
                              if it hasn't been updated.
    :param int bar_color: The color of the bar representing the value. This can
                            be a hexadecimal value for color (0x224466).
                            Default: 0x00FF00 (Solid green)
    :param int outline_color: The color of the border around the progress bar. This
                            can be a hexadecimal value for color (0x4488BB).
                            Default: 0xFFFFFF (White)
    :param int fill_color: The colour of the bar representing the remainder of the
                            value. i.e. if the current value is 42%, the 42 value
                            is represented by the bar_color parameter. The remainder,
                            58%, will be displayed in this color. This can also
                            be a hexadecimal value for color (0xEE7755).
                            Default: 0x000000 (Black)
    """

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
        """The total width of the widget"""
        return self._size[0]

    @property.getter
    def height(self):
        """The total height of the widget"""
        return self._size[1]

    @property.getter
    def x(self):
        """The horizontal (x) position of the top-left corner of the widget"""
        return self._position[0]

    @property.getter
    def y(self):
        """The vertical (y) position of the top-left corner of the widget"""
        return self._position[1]

    @property
    def progress(self):
        """The current displayed value of the widget"""
        return self._progress

    @property.setter
    def progress(self, value):
        """Sets/updates the displayed value"""
        self._progress = value
        self.render()

    def render(self):
        """The method called when the display needs to be updated. This method
        can be overridden in child classes to handle the graphics appropriately."""
        pass
