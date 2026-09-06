RESET = '\033[0m'
GREEN_FG = '\033[92m'
YELLOW_FG = '\033[93m'
RED_FG = '\033[91m'
GRAY_FG = '\033[90m'


def colorize(text, color):
    return f'{color}{text}{RESET}'


def print_success(text):
    print(colorize(text, GREEN_FG))

def print_warning(text):
    print(colorize(text, YELLOW_FG))

def print_error(text):
    print(colorize(text, RED_FG))

def print_gray(text):
    print(colorize(text, GRAY_FG))
