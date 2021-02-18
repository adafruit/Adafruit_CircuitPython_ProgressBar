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

    # pylint: disable=too-many-locals
    def render(self, _previous_value, _new_value, _progress_value) -> None:
        """
        The rendering mechanism to display the newly set value.

        :param _previous_value:  The value from which we are updating
        :type _previous_value: object
        :param _new_value: The value to which we are updating
        :type _new_value: object
        :param _progress_value: The value of the progress, or ratio between the new value and the
            maximum value
        :type _progress_value: float
        :rtype None:
        """

        _padding = self.border_thickness

        if self._margin:
            _padding += 1

        _border_thickness = self.border_thickness
        _border_size = (
            _border_thickness * 2
        )  # Size of the border on both sides of the control (1),
        # in both directions (left-to-right and top-to-bottom)

        _fill_width = (
            self.widget_width - (2 * _padding) - _border_size
        )  # Count padding on left and right
        _fill_height = (
            self.widget_height - (2 * _padding) - _border_size
        )  # Count padding on the top and bottom

        _prev_prog = float(_previous_value - self.minimum) / (
            abs(self.minimum) + abs(self.maximum)
        )

        _prev_value_size = int(_prev_prog * _fill_width)
        _new_value_size = int(_progress_value * _fill_width)

        # If we have *ANY* value other than "zero" (minimum), we should
        #   have at least one element showing
        if _new_value_size == 0 and _new_value > self.minimum:
            _new_value_size = 1

        # Conversely, if we have *ANY* value other than 100% (maximum),
        #   we should NOT show a full bar.

        if _new_value_size == _fill_height and _new_value < self.maximum:
            _new_value_size -= 1

        # Default values for increasing value
        _color = 2
        _incr = 1
        _start_offset = _padding + _border_thickness
        _start = max(_prev_value_size, _start_offset)
        _end = max(_new_value_size, 0) + _start_offset

        if _previous_value > _new_value:
            print("prev > new")
            # Remove color in range from width*value+margin to width-margin
            # from right to left
            _prev_pixel = max(2, int(self.widget_width * _previous_value - _padding))
            _new_pixel = max(int(self.widget_width * _new_value - _padding), 2)
            for _w in range(_prev_pixel, _new_pixel - 1, -1):
                for _h in range(2, self.widget_height - 2):
                    self._bitmap[_w, _h] = 0
        else:
            print("prev <= new")
            # fill from the previous x pixel to the new x pixel
            _prev_pixel = max(2, int(self.widget_width * _previous_value - 3))
            _new_pixel = min(
                int(self.widget_width * _new_value - 2),
                int(self.widget_width * 1.0 - 3),
            )
            for _w in range(_prev_pixel, _new_pixel + 1):
                for _h in range(2, self.widget_height - 2):
                    self._bitmap[_w, _h] = 2
