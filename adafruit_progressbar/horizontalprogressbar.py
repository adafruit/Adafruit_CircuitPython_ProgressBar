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
    :param progress: The percentage of the progress bar.
    :type progress: float
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
        progress=0.0,
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
            progress,
            bar_color,
            outline_color,
            fill_color,
            value,
            border_thickness=border_thickness,
            show_margin=show_margin,
            value_range=(min_value, max_value),
        )

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

        if _previous_value == _new_value:
            return  # Do nothing if there's nothing to update

        if _previous_value > _new_value:
            # Remove color in range from width*value+margin to width-margin
            # from right to left
            _prev_pixel = max(2, int(self.widget_width * self.progress - 2))
            _new_pixel = max(int(self.widget_width * _new_value - 2), 2)
            for _w in range(_prev_pixel, _new_pixel - 1, -1):
                for _h in range(2, self.widget_height - 2):
                    self._bitmap[_w, _h] = 0
        else:
            # fill from the previous x pixel to the new x pixel
            _prev_pixel = max(2, int(self.widget_width * self.progress - 3))
            _new_pixel = min(
                int(self.widget_width * _new_value - 2),
                int(self.widget_width * 1.0 - 3),
            )
            for _w in range(_prev_pixel, _new_pixel + 1):
                for _h in range(2, self.widget_height - 2):
                    self._bitmap[_w, _h] = 2
