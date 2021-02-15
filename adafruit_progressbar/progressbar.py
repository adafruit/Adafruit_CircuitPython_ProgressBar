# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`progressbar`
================================================================================

Dynamic progress bar widget for CircuitPython displays


* Author(s): Brent Rubell

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from horizontalprogressbar import HorizontalProgressBar


# pylint: disable=too-many-arguments, too-few-public-methods
class ProgressBar(HorizontalProgressBar):
    """A dynamic progress bar widget.

    :param x: The x-position of the top left corner.
    :type x: int
    :param y: The y-position of the top left corner.
    :type y: int
    :param width: The width of the progress bar.
    :type width: int
    :param height: The height of the progress bar.
    :type height: int
    :param progress: The percentage of the progress bar.
    :type progress: float
    :param bar_color: The color of the progress bar. Can be a hex
        value for color.
    :param outline_color: The outline of the progress bar. Can be a hex
        value for color.
    :type outline_color: int
    :param stroke: Used for the outline_color
    :type stroke: int
    """

    # pylint: disable=invalid-name
    def __init__(
        self,
        x,
        y,
        width,
        height,
        progress=0.0,
        bar_color=0x00FF00,
        outline_color=0xFFFFFF,
        stroke=1,
    ):

        # This needs to remain for backward compatibility, the default ProgressBar class
        # should only be able to handle values of type "float"
        assert isinstance(progress, float), "Progress must be a floating point value."

        super().__init__(
            (x, y),
            (width, height),
            progress,
            bar_color,
            outline_color,
            0x444444,
            border_thickness=stroke,
            show_margin=True,
            value_range=(0.0, 1.0),
        )

    #     _outline_color: int  # The colour used for the border of the widget

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
