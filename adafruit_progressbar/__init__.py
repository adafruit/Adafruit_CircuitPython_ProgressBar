# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`progressbar_base`
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


class ProgressBarBase(displayio.TileGrid):
    """The base class for dynamic progress bar widgets.

    :param position: The coordinates (x, y) of the top left corner
    :type position: Tuple[int, int]
    :param size: The size (width, height) of the progress bar
    :type size: Tuple[int, int]
    :param  start_value: The beginning value of the progress bar. This value
                              is displayed when the progress bar is first visible,
                              if it hasn't been updated.
    :type start_value: float
    :param bar_color: The color of the bar representing the value. This can
                            be a hexadecimal value for color (0x224466).
                            Default: 0x00FF00 (Solid green)
    :type bar_color: int
    :param outline_color: The color of the border around the progress bar. This
                            can be a hexadecimal value for color (0x4488BB).
                            Default: 0xFFFFFF (White)
    :type outline_color: int
    :param fill_color: The colour of the bar representing the remainder of the
                            value. i.e. if the current value is 42%, the 42 value
                            is represented by the bar_color parameter. The remainder,
                            58%, will be displayed in this color. This can also
                            be a hexadecimal value for color (0xEE7755).
                            Default: 0x000000 (Black)
    :type fill_color: int
    :param show_margin: Specify whether a margin between the border of the widget and the bar
                              representing the value should be visible or not.
                              Default: True
    :type show_margin: bool
    :param value_range: Specify the range of allowed values for which the progress
                        should be displayed. When setting the "value" property,
                        this range is the one against which its progression will be determined.
                        Default: (0.0, 1.0)
    :type value_range: Tuple[int, int] or Tuple[float, float]
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        position: (int, int),
        size: (int, int),
        start_value: float = 0.0,
        bar_color=0x00FF00,
        outline_color=0xFFFFFF,
        fill_color=0x000000,
        border_thickness=1,
        show_margin=False,
        value_range=(0.0, 1.0),
    ):

        self._size = size
        self._position = position
        self._progress = start_value
        self._bitmap = displayio.Bitmap(self.width, self.height, 3)
        self._palette = displayio.Palette(3)
        self._palette[0] = fill_color
        self._palette[1] = outline_color
        self._palette[2] = bar_color
        self._border_thickness = border_thickness
        self._show_margin = show_margin
        self._range = value_range

        super().__init__(
            self._bitmap,
            pixel_shader=self._palette,
            x=self._position[0],
            y=self._position[1],
        )

        self._draw_outline()

    _bitmap: displayio.Bitmap  # The bitmap used for the bar/value
    _position: (int, int)  # The (x,y) coordinates of the top-left corner
    _size: (int, int)  # The dimensions of the progress bar
    _palette: displayio.Palette(3)  # The palette to be used
    _progress: float  # The value to represent, between 0.0 and 100.0
    _border_thickness: int  # The thickness of the border around the control, in pixels
    _show_margin: bool  # Whether we should display a margin between the border and the value/bar
    # The minimum and maximum values we can represent
    _range: (int, int) or (float, float)

    @property
    def size(self):
        """The size at the outer edge of the control, returned as a tuple (width, height)"""
        return self._size

    @property
    def width(self):
        """The total width of the widget, in pixels. Includes the border and margin."""
        return self.size[0]

    @property
    def height(self):
        """The total height of the widget, in pixels. Includes the border and margin."""
        return self.size[1]

    @property
    def x(self):
        """The horizontal (x) position of the top-left corner of the widget."""
        return self._position[0]

    @property
    def y(self):
        """The vertical (y) position of the top-left corner of the widget."""
        return self._position[1]

    @property
    def progress(self):
        """Gets the current displayed value of the widget."""
        return self._progress

    @property
    def border_thickness(self):
        return self._border_thickness

    @progress.setter
    def progress(self, value):
        """The current displayed value of the widget.

        :param float value: The new value which should be displayed by the progress
                            bar. Must be between 0.0-1.0
        """
        _old_value = self._progress
        # If we're using floats, from 0.0 to 1.0, using 4 decimal places allows us to handle values as
        # precise as 0.23456, which evaluates to a percentage value of 23.45% (with rounding)
        self._progress = round(value, 4)
        self.render(_old_value, self.progress)

    @property
    def range(self):
        """The range which can be handled as a tuple (min,max)"""
        return self._range

    @property
    def minimum(self):
        """The minimum (lowest) value which can be displayed"""
        return self.range[0]

    @property
    def maximum(self):
        """The maximum (highest) value which can be displayed"""
        return self.range[1]

    def _draw_outline(self):
        """Draws the outline (border) of the progressbar, with a thickness value
        from self.border_thickness."""
        stroke = self.border_thickness

        # draw outline rectangle
        for _w in range(self.width):
            for line in range(stroke):
                self._bitmap[_w, line] = 1
                self._bitmap[_w, self.height - 1 - line] = 1
        for _h in range(self.height):
            for line in range(stroke):
                self._bitmap[line, _h] = 1
                self._bitmap[self.width - 1 - line, _h] = 1

    def render(self, _old_value, _new_value):
        """The method called when the display needs to be updated. This method
        can be overridden in child classes to handle the graphics appropriately.

        :param _old_value: float: The value from which we're updating
        :param _new_value: float: The value to which we're updating

        """

    def info():
        """This is the `info` method. It gives you info.

        This information is usefull for debugging, and
        for testing inherited documentation.
        """
