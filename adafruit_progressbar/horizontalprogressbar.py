# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`horizontalprogressbar`
================================================================================

Dynamic progress bar widget for CircuitPython displays


"""

# import displayio
from . import ProgressBarBase, FillDirection


class HorizontalProgressBar(ProgressBarBase):
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
    :param border_thickness: Used for the outline_color
    :type border_thickness: int
    :param show_margin: Whether or not to have a margin between the border and
        the fill, or not.
    :type show_margin: bool
    :param direction: The direction of the fill
    :type direction: FillDirection

    """

    # pylint: disable=bad-option-value, unused-argument, too-many-arguments
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
        border_thickness=1,
        show_margin=True,
        direction=FillDirection.DEFAULT,
    ):

        super().__init__(
            anchor_position,
            size,
            value,
            bar_color,
            outline_color,
            fill_color,
            border_thickness,
            show_margin,
            (min_value, max_value),
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

        _prev_value_size = int(_prev_ratio * self.fill_width())
        _new_value_size = int(_new_ratio * self.fill_width())

        # If we have *ANY* value other than "zero" (minimum), we should
        #   have at least one element showing
        if _new_value_size == 0 and _new_value > self.minimum:
            _new_value_size = 1

        # Conversely, if we have *ANY* value other than 100% (maximum),
        #   we should NOT show a full bar.
        if _new_value_size == self.fill_width() and _new_value < self.maximum:
            _new_value_size -= 1

        _render_offset = self.margin_size + self.border_thickness

        # Default values for increasing value
        _color = 2
        _incr = 1
        _start = max(_prev_value_size + _render_offset, _render_offset)
        _end = max(_new_value_size, 0) + _render_offset

        if _prev_value_size > _new_value_size:
            # Override defaults to be decreasing
            _color = 0  # Clear
            _incr = -1  # Iterate range downward
            _start = max(_prev_value_size + _render_offset, _render_offset)
            _end = max(_new_value_size + _render_offset, _render_offset) - 1

        for hpos in range(_start, _end, _incr):
            for vpos in range(_render_offset, _render_offset + self.fill_height()):
                self._bitmap[hpos, vpos] = _color
