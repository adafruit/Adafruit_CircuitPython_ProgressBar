# SPDX-FileCopyrightText: Copyright (c) 2020-2021 Brent Rubell for Adafruit Industries, Hugo Dahl
#
# SPDX-License-Identifier: MIT

"""
`verticalprogressbar`
================================================================================

Dynamic progress bar widget for CircuitPython displays


* Author(s): Brent Rubell, Hugo Dahl

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
import displayio
from . import ProgressBarBase, FillDirection


# pylint: disable=too-many-arguments, too-few-public-methods, too-many-instance-attributes
class VerticalProgressBar(ProgressBarBase):
    """A dynamic progress bar widget.

    The anchor position is the position where the control would start if it
    were being read visually or on paper, where the (0, 0) position is
    the lower-left corner for ascending progress bars (fills from the bottom to
    to the top in vertical bars, or from the left to the right in horizontal
    progress bars), upper-left corner for descending progress bars (fills from
    the top to the bottom).

    Using the diagrams below, the bar will fill in the following directions::

                         -----------------------------
                         | Horizontal   | Vertical   |
        ----------------------------------------------
        | Ascending      |  1-3 to 2-4 |  3-4 to 1-2 |
        ----------------------------------------------
        | Descending     |  2-4 to 1-3 |  1-2 to 3-4 |
        ----------------------------------------------

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
        value=0,
        bar_color=0x00FF00,
        outline_color=0xFFFFFF,
        fill_color=0x444444,
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

        self._x = anchor_position[0]
        self._y = anchor_position[1]

        self._stroke = stroke

        super().__init__(
            anchor_position,
            size,
            value,
            bar_color,
            outline_color,
            fill_color,
            border_thickness=stroke,
            show_margin=True,
            value_range=(min_value, max_value),
        )

    # pylint: disable=too-many-locals
    def render(self, _old_value, _new_value, _progress_value):
        """
        Does the work of actually creating the graphical representation of
            the value (percentage, aka "progress") to be displayed.

        :param _old_value: The previously displayed value
        :type _old_value: float
        :param _new_value: The new value to display
        :type _new_value: float
        :param _progress_value: The value to display, as a percentage, represented
            by a float from 0.0 to 1.0 (0% to 100%)
        :type _progress_value: float
        :return: None
        :rtype: None
        """

        _fill_height = self.fill_height()
        _fill_width = self.fill_width()

        print(f"Widget dimensions: {self.widget_width} x {self.widget_height}")
        print(f"Fill dimensions: {_fill_width} x {_fill_height}")

        _prev_ratio = _old_value / self.value_span()
        _new_ratio = _new_value / self.value_span()

        _prev_value_size = int(_prev_ratio * _fill_height)
        _new_value_size = int(_new_ratio * _fill_height)

        # If we have *ANY* value other than "zero" (minimum), we should
        #   have at least one element showing
        if _new_value_size == 0 and _new_value > self._min:
            _new_value_size = 1

        # Conversely, if we have *ANY* value other than 100% (maximum),
        #   we should NOT show a full bar.

        if _new_value_size == self.fill_height() and _new_value < self._max:
            _new_value_size -= 1

        _render_offset = 2  # TODO: Calculate in the same way as with "fill_width"

        # Default values for increasing value
        _color = 2
        _incr = 1
        _start_offset = _render_offset
        _start = max(_prev_value_size, _start_offset)
        _end = max(_new_value_size, 0) + _start_offset

        if _prev_value_size > _new_value_size:
            # Override defaults to be decreasing
            _color = 0  # Clear
            _incr = -1  # Iterate range downward
            _start_offset = _render_offset
            _start = max(_prev_value_size, _start_offset)
            _end = max(_new_value_size, _start_offset)
        elif _prev_value_size == _new_value_size:
            return  # The pre-defined values above the start
            # of the if block are already correct.
        else:
            pass  # No value change. Return.

        for h in range(_start, _end, _incr):
            for w in range(_render_offset, _fill_width + _render_offset):
                self._bitmap[w, h] = _color
