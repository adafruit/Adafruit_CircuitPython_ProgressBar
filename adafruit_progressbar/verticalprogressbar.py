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

    # Perform the rendering/drawing of the progress bar using vertical bar
    # specific logic for pixel adjustments. The added complexity is that by
    # default, the bar fills from bottom to top, which is a _descending_ value of
    # the **Y** axis, versus an ascending value for the default horizontal
    # progress bar direction.

    def render(
        self,
        _old_value: Union[int, float],
        _new_value: Union[int, float],
        _progress_value: float,
    ) -> None:
        """
        Does the work of actually creating the graphical representation of
            the value (percentage, aka "progress") to be displayed.

        :param _old_value: The previously displayed value
        :type _old_value: int/float
        :param _new_value: The new value to display
        :type _new_value: int/float
        :param _progress_value: The value to display, as a percentage, represented
            by a float from 0.0 to 1.0 (0% to 100%)
        :type _progress_value: float
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

        if _old_value_size >= _new_value_size:
            # Override defaults to be decreasing
            _color = 0  # Clear
            _incr = -1  # Iterate range downward
            _start = max(_old_value_size + _render_offset, _render_offset)
            _end = max(_new_value_size + _render_offset, _render_offset) - 1
            # If we're setting to minimum, make sure we're clearing by
            # starting one "bar" higher
            if _new_value == self.minimum:
                _start += 1

        if self._direction == VerticalFillDirection.BOTTOM_TO_TOP:
            _ref_pos = self.widget_height - 1
            _end = _ref_pos - _end  # Those pesky "off-by-one" issues
            _start = _ref_pos - _start
            _incr = -1 if _start > _end else 1
            _color = 0 if _old_value > _new_value else 2

        for vpos in range(_start, _end, _incr):
            for hpos in range(_render_offset, _render_offset + self.fill_width()):
                self._bitmap[hpos, vpos] = _color
