# -*- coding: utf-8 -*-

palette = ["#15527F", "#FF9900", "#FFCC00", "#0099CC", "#999900", "#663366",
           "#FF0000", "#33CC99", "#006600", "#663300", "#99CC00", "#FF0033"]
color_num = 0


class Colors():
    """
    Class to handle colors for charts
    """

    def __init__(self, df=None):
        """
        Initialize
        """
        self.color_index = 0

    def color_(self, i=None):
        """
        Get a color from the palette
        """
        global palette, color_num
        if i is not None:
            color_num = i
        if color_num == len(palette) - 1:
            color_num = 0
        res = palette[color_num]
        color_num += 1
        return res

    def scolor(self):
        """
        Set a unique color from a serie
        """
        global palette
        color = palette[self.color_index]
        if len(palette) - 1 == self.color_index:
            self.color_index = 0
        else:
            self.color_index += 1
        self.color(color)
