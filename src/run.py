import argparse

from words import load_words
from game import play, ask_play_again, shuffled_words
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
    for word in shuffled_words(answers):
        if not (play(answers, accepted, hard=args.hard, word=word)
                and ask_play_again()):
            break


if __name__ == '__main__':
    main()
