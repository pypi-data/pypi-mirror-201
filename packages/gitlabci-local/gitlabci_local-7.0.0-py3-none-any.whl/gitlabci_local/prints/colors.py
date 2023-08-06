#!/usr/bin/env python3

# Modules libraries
from colored import attr, colored, fg

# Colors class, pylint: disable=too-few-public-methods
class Colors:

    # Attributes
    ALL = []
    BOLD = ''
    CYAN = ''
    GREEN = ''
    GREY = ''
    RED = ''
    RESET = ''
    YELLOW = ''
    YELLOW_LIGHT = ''

    # Enabled
    @staticmethod
    def enabled() -> bool:

        # Result
        return colored('').enabled()

    # Prepare
    @staticmethod
    def prepare() -> None:

        # Colors enabled
        if Colors.enabled():
            Colors.BOLD = attr('reset') + attr('bold')
            Colors.CYAN = fg('cyan') + attr('bold')
            Colors.GREEN = fg('green') + attr('bold')
            Colors.GREY = fg('light_gray') + attr('bold')
            Colors.RED = fg('red') + attr('bold')
            Colors.RESET = attr('reset')
            Colors.YELLOW = fg('yellow') + attr('bold')
            Colors.YELLOW_LIGHT = fg('light_yellow') + attr('bold')
            Colors.ALL = [
                Colors.BOLD,
                Colors.CYAN,
                Colors.GREEN,
                Colors.GREY,
                Colors.RED,
                Colors.RESET,
                Colors.YELLOW,
                Colors.YELLOW_LIGHT,
            ]

        # Colors disabled
        else:
            Colors.BOLD = ''
            Colors.CYAN = ''
            Colors.GREEN = ''
            Colors.GREY = ''
            Colors.RED = ''
            Colors.RESET = ''
            Colors.YELLOW = ''
            Colors.YELLOW_LIGHT = ''
            Colors.ALL = []
