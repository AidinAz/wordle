import os
import sys

RESET = '\033[0m'
GREEN_FG = '\033[92m'
YELLOW_FG = '\033[93m'
RED_FG = '\033[91m'
GRAY_FG = '\033[90m'

CLEAR = '\033[H\033[J'


def _is_terminal() -> bool:
    try:
        return sys.stdout.isatty()
    except (AttributeError, ValueError):
        return False


def _detect_colour() -> bool:
    if os.environ.get('NO_COLOR'):
        return False
    if os.environ.get('TERM') == 'dumb':
        return False
    if os.environ.get('FORCE_COLOR'):
        return True
    return _is_terminal()


def _detect_screen_control() -> bool:
    return os.environ.get('TERM') != 'dumb' and _is_terminal()

_COLOUR = _detect_colour()
_SCREEN = _detect_screen_control()


def use_colour() -> bool:
    return _COLOUR


def use_screen_control() -> bool:
    return _SCREEN


def clear_sequence() -> str:
    """Escape codes that reset the frame, or '' when the screen is not ours."""
    return CLEAR if _SCREEN else ''


def colorize(text, color):
    return f'{color}{text}{RESET}' if _COLOUR else text


def print_success(text):
    print(colorize(text, GREEN_FG))

def print_warning(text):
    print(colorize(text, YELLOW_FG))

def print_error(text):
    print(colorize(text, RED_FG))

def print_gray(text):
    print(colorize(text, GRAY_FG))
