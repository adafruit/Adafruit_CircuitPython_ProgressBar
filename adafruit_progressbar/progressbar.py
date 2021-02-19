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
from adafruit_progressbar.horizontalprogressbar import HorizontalProgressBar


# pylint: disable=too-many-arguments, too-few-public-methods
class ProgressBar(HorizontalProgressBar):
    """A dynamic progress bar widget.

    NOTE: This class is made available for backward compatibility with v1.x of
    the adafruit_progressbar library. New uses should not use this class, but
    instead, use its successor, HorizontalProgressBar.

    :param x: The x-position of the top left corner.
    :type x: int
    :param y: The y-position of the top left corner.
    :type y: int
    :param width: The width of the progress bar.
    :type width: int
    :param height: The height of the progress bar.
    :type height: int
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
            0,
            100,
            (progress * 100),  # Progress vs. max above
            bar_color,
            outline_color,
            0x000000,
            border_thickness=stroke,
            show_margin=True,
        )

    # Override the base "progress" property to correctly handle values
    # in the v1 range of 0.0-1.0
    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        root_value = value * 100
        if root_value == self.value:
            return
        self.value = root_value
