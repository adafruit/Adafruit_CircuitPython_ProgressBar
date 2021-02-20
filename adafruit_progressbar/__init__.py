# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`progressbar_base`
================================================================================

Dynamic progress bar widget for CircuitPython displays


* Author(s): Brent Rubell and Hugo Dahl

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
import displayio


class ProgressBarBase(displayio.TileGrid):
    """The base class for dynamic progress bar widgets.

    :param position: The coordinates (x, y) of the top left corner
    :type position: Tuple[int, int]
    :param size: The size (width, height) of the progress bar
    :type size: Tuple[int, int]
    :param bar_color: The color of the bar representing the value. This can
                            be a hexadecimal value for color (0x224466).
                            Default: 0x00FF00 (Solid green)
    :type bar_color: int
    :param border_color: The color of the border around the progress bar. This
                            can be a hexadecimal value for color (0x4488BB).
                            Default: 0xFFFFFF (White)
    :type border_color: int
    :param fill_color: The colour of the bar representing the remainder of the
                            value. i.e. if the current value is 42%, the 42 value
                            is represented by the bar_color parameter. The remainder,
                            58%, will be displayed in this color. This can also
                            be a hexadecimal value for color (0xEE7755).
                            Default: 0x000000 (Black)
    :type fill_color: int
    :param margin_size: Specify whether a margin between the border of the widget and the bar
                              representing the value should be visible or not.
                              Default: True
    :type margin_size: bool
    :param value_range: Specify the range of allowed values for which the progress
                        should be displayed. When setting the "value" property,
                        this range is the one against which its progression will be determined.
                        Default: (0.0, 1.0)
    :type value_range: Tuple[int, int] or Tuple[float, float]
    """

    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(
        self,
        position,
        size,
        value=0,
        bar_color=0x00FF00,
        border_color=0xFFFFFF,
        fill_color=0x000000,
        border_thickness=1,
        margin_size=1,
        value_range=(0, 100),
    ):

        assert (
            value_range[0] < value_range[1]
        ), "The minimum value must be less than the maximum value"

        assert (
            size[0] > 0 and size[1] > 0
        ), "The width and the height must be greater than zero"

        assert (
            value_range[0] <= value <= value_range[1]
        ), "The starting value must be within the range of minimum to maximum"

        _edge_size = 2 * margin_size + 2 * border_thickness

        assert _edge_size < size[0], (
            "The size of the borders and margins combined must be "
            "less than the width of the widget"
        )

        assert _edge_size < size[1], (
            "The size of the borders and margins combined must be "
            "less than the height of the widget"
        )

        self._progress = 0.0
        self._widget_size = size
        self._position = position

        self._bitmap = displayio.Bitmap(size[0], size[1], 3)
        self._palette = displayio.Palette(3)
        self._border_thickness = border_thickness
        self._margin_size = margin_size
        self._range = value_range
        self._progress = 0.0

        self._old_value = self.minimum
        self._value = self.minimum

        self.fill = fill_color
        self.bar_color = bar_color
        self.border_color = border_color

        # Setup value and old_value to handle the change to the new
        # initial value later.
        self._value = self.minimum
        self._old_value = self.minimum

        super().__init__(
            self._bitmap,
            pixel_shader=self._palette,
            x=self._position[0],
            y=self._position[1],
        )

        self._draw_outline()
        self.value = value

    #     _bitmap: displayio.Bitmap  # The bitmap used for the bar/value
    #     _position: (int, int)  # The (x,y) coordinates of the top-left corner
    #     _widget_size: (int, int)  # The dimensions of the progress bar
    #     _palette: displayio.Palette(3)  # The palette to be used
    #     _progress: float  # The value to represent, between 0.0 and 100.0
    #     _border_thickness: int  # The thickness of the border around the control, in pixels
    #     _margin_size: bool  # Whether we should display a margin between
    #       the border and the value/bar
    #     # The minimum and maximum values we can represent
    #     _range: (int, int) or (float, float)

    #     Color palette index to property mapping:
    #       0:  Bar fill color
    #       1:  Border color
    #       2:  Background fill color

    @property
    def widget_size(self):
        """The size at the outer edge of the control, returned as a tuple (width, height)"""
        return self._widget_size

    @property
    def widget_width(self):
        """The total width of the widget, in pixels. Includes the border and margin."""
        return self.widget_size[0]

    @property
    def border_thickness(self):
        """Gets the currently configured thickness of the border (in pixels)"""
        return self._border_thickness

    @property
    def widget_height(self):
        """The total height of the widget, in pixels. Includes the border and margin."""
        return self.widget_size[1]

    @property
    def border_color(self):
        """Returns the currently configured value for the color of the
        outline (border) of the widget."""
        return self._border_color

    @border_color.setter
    def border_color(self, color):
        """Sets the color of the border of the widget. Set it to 'None'
        if a border should still be part of the widget but not displayed.

        :param color: The color to be used for the border
        :type int/None:
        """

        assert (
            isinstance(color, int) or color is None
        ), "A color must be represented by a integer value"

        self._border_color = color

        if color is None:
            self._palette[1] = 0x00
            self._palette.make_transparent(1)
        else:
            self._palette[1] = color
            self._palette.make_opaque(1)

    @property
    def fill(self):
        """The fill of the progress bar. Can be a hex value for a color or ``None`` for
        transparent.
        """
        return self._fill_color

    @fill.setter
    def fill(self, color):
        """Sets the fill of the progress bar. Can be a hex value for a color or ``None`` for
        transparent.
        """
        self._fill_color = color
        if color is None:
            self._palette[0] = 0x00
            self._palette.make_transparent(0)
        else:
            self._palette[0] = color
            self._palette.make_opaque(0)

    @property
    def bar_color(self):
        """The color of the bar's fill

        :returns int/None:
        """

        return self._bar_color

    @bar_color.setter
    def bar_color(self, color):
        """Sets the color of the bar

        :param color: The color to use for the bar
        :type color: int/None
        """

        self._bar_color = color

        if color is None:
            self._palette[2] = 0x00
            self._palette.make_transparent(2)
        else:
            self._palette[2] = color
            self._palette.make_opaque(2)

    @property
    def value(self):
        """
        The current value of the control, used to determine its progress/ratio
        :return: int/float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the current value of the progress within the min-max range

        :param value: The new value for the progress status
        :type value: int/float
        """

        assert isinstance(
            value, (int, float)
        ), "The value to set must be either an integer or a float"

        # Save off the previous value, so we can pass it in the
        # call to "Render"
        self._old_value = self._value
        self._value = value
        # Convert value to float since we may be dealing with
        # integer types, and we can't work with integer division
        # to get a ratio (position) of "value" within range.
        self._set_progress(self.get_value_ratio(value))

    @property
    def progress(self):
        """Gets the current displayed value of the widget.

        :return: The current progress ratio
        :rtype: float
        """
        return self._progress

    @progress.setter
    def progress(self, value):
        """Sets the current displayed value of the widget.

        :param value: The new value which should be displayed by the progress
                            bar. Must be between 0.0-1.0
        :type value: float
        """

        self._set_progress(value)

    # Bit of a hack to be able to work around the shim "ProgressBar" class
    # to be able to handle values as it used to.
    def _set_progress(self, value):
        """Sets the value for the underlying variable _progress, then
        calls self.render() with the appropriate values.

        :param value: The value to which self.progress should be set
        :type value: float
        :return: None
        """

        self._progress = round(value, 4)
        self.render(self._old_value, self._value, value)

    @property
    def range(self):
        """The range which can be handled as a Tuple(min,max)"""
        return self._range

    @property
    def minimum(self):
        """The minimum (lowest) value which can be displayed"""
        return self.range[0]

    @property
    def maximum(self):
        """The maximum (highest) value which can be displayed"""
        return self.range[1]

    def _draw_outline(self):
        """Draws the outline (border) of the progressbar, with a thickness value
        from self.border_thickness.
        :rtype None:
        """
        stroke = self.border_thickness

        # draw outline rectangle
        for _w in range(self.widget_width):
            for line in range(stroke):
                self._bitmap[_w, line] = 1
                self._bitmap[_w, self.widget_height - 1 - line] = 1
        for _h in range(self.widget_height):
            for line in range(stroke):
                self._bitmap[line, _h] = 1
                self._bitmap[self.widget_width - 1 - line, _h] = 1

    def fill_width(self):
        """Returns the amount of horizontal space within the widget
        which can be used for value display. This is typically the
        width of the widget as defined, minus any visually reserved space.
        :return int:
        """

        return self.widget_width - self._get_fill_border_size()

    def fill_height(self):
        """Returns the amount of vertical space within the widget
        which can be used for value display. This is typically the
        width of the widget as defined, minus any visually reserved
        space.
        :return int:
        """

        return self.widget_height - self._get_fill_border_size()

    def _get_fill_border_size(self):
        """Determines any visual space reserved for the widget
        based on the defined border thickness, and whether a margin
        should be placed between the border and the bar.
        The value is calculated as (2 x border_thickness) minus
        (2 x margin_size). The value for margin_size is either 0 (zero)
        or 1 (one) depending on the value of margin_size when the
        widget was created.
        :return int:
        """

        return (2 * self.border_thickness) + (2 * self.margin_size)

    @property
    def margin_size(self):
        """Returns the size of the margin on a single side of the display
        :return int:
        """
        return self._margin_size

    @margin_size.setter
    def margin_size(self, value):
        """Sets the new size of the margin to be used between the border
        (if displayed) and the value bar.

        :param value: The new size of the margin between the border
        and value bar on all sides of the widget.
        :type value: int
        """

        assert isinstance(value, int), "The margin size must be an integer"

        margin_spacing = (2 * value) + (2 * self._border_thickness)

        assert margin_spacing < self.widget_width, (
            "The size of the borders and margins combined can total the same or more"
            "than the widget's width."
        )

        assert margin_spacing < self.widget_height, (
            "The size of the borders and margins combined can total the same or more"
            "than the widget's height."
        )

        self._margin_size = value
        self._set_progress(self._progress)  # For a render pass

    def get_value_ratio(self, value):
        """Gets the ratio (percentage) of a given value within the
        range of self.minimum and self.maximum.

        :param value: The value for which the ration should be calculated
        :type value: int/float

        :return: The ratio of value:range
        :rtype: float
        """

        if self.maximum == self.minimum:
            return 0.0

        return (float(value) - self.minimum) / (self.maximum - self.minimum)

    def render(self, _old_value, _new_value, _progress_value) -> None:
        """The method called when the display needs to be updated. This method
        can be overridden in child classes to handle the graphics appropriately.

        :param _old_value: The value from which we're updating
        :type _old_value: float
        :param _new_value: The value to which we're updating
        :type _new_value: float
        :param _progress_value: The value of the progress, or ratio between the new value and the
            maximum value
        :type _progress_value: float
        :rtype None:
        """
