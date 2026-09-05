from words import load_words
from game import play


def main():
    answers, accepted = load_words()
    play(answers, accepted)


if __name__ == '__main__':
    main()
