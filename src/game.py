import random
from collections import Counter
from display import (colorize, print_success, print_warning,
                     GREEN_FG, YELLOW_FG, GRAY_FG)
from config import WORD_LENGTH, MAX_TRIES

GREEN, YELLOW, GRAY = 'green', 'yellow', 'gray'

COLOUR_CODES = {GREEN: GREEN_FG, YELLOW: YELLOW_FG, GRAY: GRAY_FG}


def score_guess(word: str, guess: str) -> list[str]:
    
    result = [GRAY] * len(guess)
    remaining = Counter()

    for i, (w_letter, g_letter) in enumerate(zip(word, guess)):
        if w_letter == g_letter:
            result[i] = GREEN
        else:
            remaining[w_letter] += 1

    for i, g_letter in enumerate(guess):
        if result[i] == GRAY and remaining[g_letter] > 0:
            result[i] = YELLOW
            remaining[g_letter] -= 1

    return result


def render_row(guess: str, colours: list[str]) -> str:
    return ' '.join(colorize(g_letter.upper(), COLOUR_CODES[colour])
                    for g_letter, colour in zip(guess, colours))


def print_board(history: list[tuple[str, list[str]]]) -> None:
    print()
    for guess, colours in history:
        print(render_row(guess, colours))
    print()


def play(answers: list[str], accepted: set[str], word_length: int = WORD_LENGTH,
         max_tries: int = MAX_TRIES) -> None:
    word = random.choice(answers)
    number_try = 0
    history: list[tuple[str, list[str]]] = []

    while True:
        prompt = (f'Guess {number_try + 1}/{max_tries} — enter a {word_length} '
                  f'letter word (or q to exit): ')
        try:
            guess = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            print(f'Goodbye! The word was "{word}".')
            break

        if guess == 'q':
            print(f'Goodbye! The word was "{word}".')
            break

        if len(guess) != word_length:
            print_warning(f'Word must have {word_length} letters. You entered {len(guess)}!')
            continue

        if guess not in accepted:
            print_warning(f'Word "{guess}" is not in the list of valid words!')
            continue

        history.append((guess, score_guess(word, guess)))
        print_board(history)

        if guess == word:
            print_success(f'Congratulations! You guessed the word "{word}" in {number_try + 1} tries!')
            break

        number_try += 1
        if number_try >= max_tries:
            print(f'You have used all your tries! The word was "{word}".')
            break
