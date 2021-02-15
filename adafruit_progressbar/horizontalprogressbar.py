# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`horizontalprogressbar`
================================================================================

Dynamic progress bar widget for CircuitPython displays


"""

# import displayio
from . import ProgressBarBase  # , FillDirection


class HorizontalProgressBar(ProgressBarBase):
    """
    A progress bar that goes horizontally.
    """

    def __init__(self):
        """
        Get stuff, horizontally!
        :param args:
        :param kwargs:
        """

        super().__init__((0, 0), (100, 20), 0.0)

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
