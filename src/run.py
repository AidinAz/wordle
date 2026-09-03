from config import WORD_LENGTH
from words import load_words
from game import play


def main():
    words = load_words()
    play(words, WORD_LENGTH)


if __name__ == '__main__':
    main()
