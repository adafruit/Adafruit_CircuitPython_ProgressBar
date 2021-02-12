# Copyright (C) 2021 Hugo Dahl for Adafruit Industries
# Copyright (c) 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`verticalprogressbar`
================================================================================

Dynamic progress bar widget for CircuitPython displays


* Author(s): Brent Rubell
                Hugo Dahl

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
import displayio
from . import ProgressBarBase


# pylint: disable=too-few-public-methods
class FillDirection(enumerate):
    """Enums to define the direction in which the progressbar
    should fill"""

    LEFT_TO_RIGHT = 0
    DEFAULT = LEFT_TO_RIGHT
    BOTTOM_UP = 1
    TOP_DOWN = 2
    RIGHT_TO_LEFT = 3


# pylint: disable=too-many-arguments, too-few-public-methods, too-many-instance-attributes
class VerticalProgressBar(ProgressBarBase):
    """A dynamic progress bar widget.

    The anchor position is the position where the control would start if it
    were being read visually or on paper, where the (0, 0) position is
    the lower-left corner for ascending progress bars (fills from the bottom to
    to the top in vertical bars, or from the left to the right in horizontal
    progress bars), upper-left corner for descending progress bars (fills from
    the top to the bottom).::

        Vertical            Horizontal

        1--2                1-----------------------2
        |  |                |                       |
        |  |                |                       |
        |  |                3-----------------------4
        |  |
        3--4

    :param anchor_position: The anchor coordinates of the progress bar.
    :type anchor_position: Tuple[int, int]
    :param size: The size in (width, height) of the progress bar
    :type size: Tuple[int, int]
    :param progress: The percentage of the progress bar.
    :type progress: float
    :param bar_color: The color of the progress bar. Can be a hex
        value for color.
    :param outline_color: The outline of the progress bar. Can be a hex
        value for color.
    :type outline_color: int
    :param stroke: Used for the outline_color
    :type stroke: int
    :param margin: Whether or not to have a margin between the border and
        the fill, or not.
    :type margin: bool
    :param direction: The direction of the fill
    :type direction: FillDirection

    """

    # pylint: disable=invalid-name
    def __init__(
        self,
        anchor_position,
        size,
        min_value=0,
        max_value=100,
        progress=0.0,
        bar_color=0x00FF00,
        outline_color=0xFFFFFF,
        stroke=1,
        margin=False,
        direction=FillDirection.DEFAULT,
    ):
        assert (
            min_value < max_value
        ), "The minimum value must be LESS THAN the maximum value"
        assert isinstance(
            anchor_position, tuple
        ), "The anchor_position must be a tuple/coordinate)"
        assert isinstance(size, tuple), "The size must be a tuple/coordinate)"

        print(f"Fill direction: {direction}")

        self._width = size[0]
        self._height = size[1]

        self._min = min_value
        self._max = max_value

        self._margin = margin

        self._bitmap = displayio.Bitmap(self._width, self._height, 3)
        self._palette = displayio.Palette(3)
        self._palette[0] = 0x0
        self._palette[1] = outline_color
        self._palette[2] = bar_color

        # _width and _height are already in use for blinka TileGrid
        self._bar_width = self._width
        self._bar_height = self._height

        self._progress_val = 0.0
        self.progress = self._progress_val
        self.progress = progress

        self._x = anchor_position[0]
        self._y = anchor_position[1]

        # draw outline rectangle
        for _w in range(self._width):
            for line in range(stroke):
                self._bitmap[_w, line] = 1
                self._bitmap[_w, self._height - 1 - line] = 1
        for _h in range(self._height):
            for line in range(stroke):
                self._bitmap[line, _h] = 1
                self._bitmap[self._width - 1 - line, _h] = 1

        # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
        super().__init__(self._bitmap, pixel_shader=self._palette, x=self._x, y=self._y)

    @property
    def progress(self):
        """The percentage of the progress bar expressed as a
        floating point number.

        """
        return self._progress_val

    # pylint: disable=too-many-locals
    @progress.setter
    def progress(self, value):
        """Draws the progress bar

        :param value: Progress bar value.
        :type value: float
        """
        assert value <= self._max, "Progress value may not be > maximum value"
        assert value >= self._min, "Progress value may not be < minimum value"

        _new_value = round(value / self._max, 2)
        _padding = 1

        if self._margin:
            _padding = 1

        _border_thickness = 1
        _border_size = (
            _border_thickness * 2
        )  # Size of the border on both sides of the control (1),
        # in both directions (left-to-right and top-to-bottom)

        _fill_width = (
            self.width - (2 * _padding) - _border_size
        )  # Count padding on left and right
        _fill_height = (
            self.height - (2 * _padding) - _border_size
        )  # Count padding on the top and bottom

        _prev_value_size = int(self._progress_val * _fill_width)
        _new_value_size = int(_new_value * _fill_width)

        # If we have *ANY* value other than "zero" (minimum), we should
        #   have at least one element showing
        if _new_value_size == 0 and value > self._min:
            _new_value_size = 1

        # Conversely, if we have *ANY* value other than 100% (maximum),
        #   we should NOT show a full bar.

        if _new_value_size == _fill_width and value < self._max:
            _new_value_size -= 1

        # Default values for increasing value
        _color = 2
        _incr = 1
        _start_offset = _padding + _border_thickness
        _start = max(_prev_value_size, _start_offset)
        _end = max(_new_value_size, 0) + _start_offset

        if _prev_value_size > _new_value_size:
            # Override defaults to be decreasing
            _color = 0  # Clear
            _incr = -1  # Iterate range downward
            _start_offset = _padding + _border_thickness
            _start = max(_prev_value_size, _start_offset)
            _end = max(_new_value_size, _start_offset)
        elif _prev_value_size == _new_value_size:
            return  # No action to take. Return
        else:
            pass

        # DEBUG
        print(
            f"Start: {_start}  End: {_end}  Incr: {_incr}  Size: {_new_value_size}  Color: {_color}"
        )

        # Because range() is ( from-include, to-exclude )...

        _vert_start = _border_thickness + _padding
        _vert_end = _vert_start + _fill_height

        for h in range(_vert_start, _vert_end):
            for w in range(_start, _end, _incr):
                self._bitmap[w, h] = _color

        self._progress_val = _new_value

    @property
    def fill(self):
        """The fill of the progress bar. Can be a hex value for a color or ``None`` for
        transparent.

        """
        return self._palette[0]

    @property
    def width(self):
        """The width of the progress bar. In pixels, includes the border."""
        return self._bar_width

    @property
    def height(self):
        """The height of the progress bar. In pixels, includes the border."""
        return self._bar_height

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
