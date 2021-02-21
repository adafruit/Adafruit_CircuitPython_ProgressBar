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
from enum import Enum
from . import ProgressBarBase


class VerticalFillDirection(Enum):
    """This enum is used to specify the direction in which the progress
    bar's display bar should fill as the value represented increases."""

    BOTTOM_TO_TOP = 0, "Fills from the bottom up toward the top"
    DEFAULT = BOTTOM_TO_TOP, "Default fill direction (BOTTOM_TO_TOP)"
    TOP_TO_BOTTOM = 1, "Fills from the top down toward the bottom"


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
    :param bar_color: The color of the progress bar. Can be a hex
        value for color.
    :param outline_color: The outline of the progress bar. Can be a hex
        value for color.
    :type outline_color: int
    :param stroke: Used for the outline_color
    :type stroke: int
    :param margin_size: Whether or not to have a margin between the border and
        the fill, or not.
    :type margin_size: int
    :param direction: The direction of the fill
    :type direction: VerticalFillDirection

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
        margin_size=1,
        direction=VerticalFillDirection.DEFAULT,
    ):

        self._direction = direction

        super().__init__(
            anchor_position,
            size,
            value,
            bar_color,
            outline_color,
            fill_color,
            border_thickness=stroke,
            margin_size=margin_size,
            value_range=(min_value, max_value),
        )

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

        _prev_ratio = self.get_value_ratio(_old_value)
        _new_ratio = self.get_value_ratio(_new_value)

        _old_value_size = int(_prev_ratio * self.fill_height())
        _new_value_size = int(_new_ratio * self.fill_height())

        # If we have *ANY* value other than "zero" (minimum), we should
        #   have at least one element showing
        if _new_value_size == 0 and _new_value > self.minimum:
            _new_value_size = 1

        # Conversely, if we have *ANY* value other than 100% (maximum),
        #   we should NOT show a full bar.
        if _new_value_size == self.fill_height() and _new_value < self.maximum:
            _new_value_size -= 1

        _render_offset = self.margin_size + self.border_thickness

        # Default values for increasing value
        _color = 2
        _incr = 1
        _start = max(_old_value_size + _render_offset, _render_offset)
        _end = max(_new_value_size, 0) + _render_offset

        if _old_value_size > _new_value_size:
            # Override defaults to be decreasing
            _color = 0  # Clear
            _incr = -1  # Iterate range downward
            _start = max(_old_value_size + _render_offset, _render_offset)
            _end = max(_new_value_size + _render_offset, _render_offset) - 1

        if self._direction == VerticalFillDirection.BOTTOM_TO_TOP:
            _ref_pos = self.widget_height - 1
            _end = _ref_pos - _end  # Those pesky "off-by-one" issues
            _start = _ref_pos - _start
            _incr = -1 if _start > _end else 1
            _color = 0 if _old_value > _new_value else 2

        for vpos in range(_start, _end, _incr):
            for hpos in range(_render_offset, _render_offset + self.fill_width()):
                self._bitmap[hpos, vpos] = _color
