palette = ["#15527F", "#FF9900", "#FFCC00", "#0099CC", "#999900", "#663366",
           "#FF0000", "#33CC99", "#006600", "#663300", "#99CC00", "#FF0033"]
color_num = 0


class Colors():
    """
    Class to handle colors for charts
    """

    def color(self):
        """
        Get a color from the palette
        """
        global palette, color_num
        if color_num == len(palette) - 1:
            color_num = 0
        res = palette[color_num]
        color_num += 1
        return res
