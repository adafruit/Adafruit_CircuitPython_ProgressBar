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

try:
    from typing import Tuple, Union
except ImportError:
    pass  # Not needed for execution
from . import ProgressBarBase


# pylint: disable=too-few-public-methods
class VerticalFillDirection:
    """This enum is used to specify the direction in which the progress
    bar's display bar should fill as the value represented increases."""

    # pylint: disable=pointless-string-statement
    """Fills from the bottom up toward the top"""
    BOTTOM_TO_TOP = 0
    # pylint: disable=pointless-string-statement
    """Default fill direction (BOTTOM_TO_TOP)"""
    DEFAULT = BOTTOM_TO_TOP
    # pylint: disable=pointless-string-statement
    """Fills from the top down toward the bottom"""
    TOP_TO_BOTTOM = 1


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

        --------------------------------
        | Bottom-to-top  |  3-4 to 1-2 |
        --------------------------------
        | Top-to-bottom  |  1-2 to 3-4 |
        --------------------------------

        1--2
        |  |
        |  |
        |  |
        |  |
        3--4

    :param position: The coordinates of the top-left corner of progress bar.
    :type position: Tuple[int, int]
    :param size: The size in (width, height) of the progress bar, in pixels
    :type size: Tuple[int, int]
    :param min_value: The lowest value which can be displayed by the progress bar.
        When the "value" property is set to the same value, no bar is displayed.
    :type min_value: int, float
    :param max_value:  This highest value which can be displayed by the progress bar.
        When the "value" property is set to the same value, the bar shows as full.
    :type max_value: int, float
    :param value: The starting value to be displayed. Must be between the values of
        min_value and max_value, inclusively.
    :type value: int, float
    :param bar_color: The color of the value portion of the progress bar.
        Can be a hex value for color (i.e. 0x225588).
    :type bar_color: int, Tuple[byte, byte, byte]
    :param outline_color: The colour for the outline of the progress bar.
        Can be a hex value for color (i.e. 0x225588).
    :type outline_color: int, Tuple[byte, byte, byte]
    :param fill_color: The colour for the background within the progress bar.
        Can be a hex value for color (i.e. 0x225588).
    :type fill_color: int, Tuple[byte, byte, byte]
    :param border_thickness: The thickness of the outer border of the widget. If it is
        1 or larger, will be displayed with the color of the "outline_color" parameter.
    :type border_thickness: int
    :param margin_size: The thickness (in pixels) of the margin between the border and
        the bar. If it is 1 or larger, will be filled in by the color of the
        "fill_color" parameter.
    :type margin_size: int
    :param direction: The direction of the fill
    :type direction: VerticalFillDirection

    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int],
        min_value: Union[int, float] = 0,
        max_value: Union[int, float] = 100,
        value: Union[int, float] = 0,
        bar_color: Union[int, Tuple[int, int, int]] = 0x00FF00,
        outline_color: Union[int, Tuple[int, int, int]] = 0xFFFFFF,
        fill_color: Union[int, Tuple[int, int, int]] = 0x444444,
        border_thickness: int = 1,
        margin_size: int = 1,
        direction: VerticalFillDirection = VerticalFillDirection.DEFAULT,
    ) -> None:

        # Store the "direction" value locally. While they may appear to
        # "relate" with the values of the horizontal bar, their handling
        # is too different to be stored in the same underlying property,
        # which could lead to confusion
        self._direction = direction

        super().__init__(
            position,
            size,
            value,
            bar_color,
            outline_color,
            fill_color,
            border_thickness,
            margin_size,
            (min_value, max_value),
        )

    def _get_sizes_min_max(self) -> Tuple[int, int]:
        return 0, self.fill_height()

    def _get_value_sizes(self, _old_ratio: float, _new_ratio: float) -> Tuple[int, int]:
        return int(_old_ratio * self.fill_height()), int(
            _new_ratio * self.fill_height()
        )

    def _get_vertical_fill(
        self, _start: int, _end: int, _incr: int
    ) -> Tuple[int, int, int]:
        return _start, _end, _incr

    def _invert_fill_direction(self) -> bool:
        return self._direction == VerticalFillDirection.BOTTOM_TO_TOP
