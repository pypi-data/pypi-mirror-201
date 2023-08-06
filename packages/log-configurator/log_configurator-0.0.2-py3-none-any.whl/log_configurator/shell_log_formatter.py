"""
Log formatter that prints colored to shell.
"""
import logging


class ColoredShellLogFormatter(logging.Formatter):
    """
    Formatter class.
    """
    SHELL_COLORS = {
        "NONE": '\033[0m',
        "DEBUG": '\033[0m',
        "INFO": '\033[0m',
        "HIGHLIGHT": '\033[36m',
        "WARNING": '\033[33m',
        "ERROR": '\033[31m',
    }

    def __init__(self, colors, fmt, style='%'):
        super().__init__(fmt=fmt, style=style)
        self.formatters = {}
        self.default_formatter = logging.Formatter(
            "Requested Formatter not found! - {module}: {message}", style=style)
        for loglevel in colors:
            self.formatters[loglevel] = logging.Formatter(
                ColoredShellLogFormatter.colorize(fmt, colors[loglevel]), style=style)

    def format(self, record):
        formatter = self.formatters.get(record.levelname, self.default_formatter)
        return formatter.format(record)

    @staticmethod
    def colorize(text, color_name):
        """
        Colorizes text.
        :param text: Text to colorize
        :param color_name: Color to use, check SHELL_COLORS
        :return: Colorized text
        """
        return color_name + text + ColoredShellLogFormatter.SHELL_COLORS['NONE']
