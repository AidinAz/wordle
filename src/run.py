import argparse

from words import load_words
from game import play
from config import HARD_MODE


def parse_args():
    parser = argparse.ArgumentParser(description='Play Wordle in your terminal.')
    parser.add_argument('--hard', action=argparse.BooleanOptionalAction,
                        default=HARD_MODE,
                        help='hard mode: every revealed hint must be reused')
    return parser.parse_args()


def main():
    args = parse_args()
    answers, accepted = load_words()
    play(answers, accepted, hard=args.hard)


if __name__ == '__main__':
    main()
