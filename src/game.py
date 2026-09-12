import random
from collections import Counter
from display import (colorize, print_success, print_warning,
                     GREEN_FG, YELLOW_FG, GRAY_FG)
from config import WORD_LENGTH, MAX_TRIES, HARD_MODE

GREEN, YELLOW, GRAY = 'green', 'yellow', 'gray'

COLOUR_CODES = {GREEN: GREEN_FG, YELLOW: YELLOW_FG, GRAY: GRAY_FG}

COLOUR_RANK = {GRAY: 0, YELLOW: 1, GREEN: 2}

KEYBOARD_ROWS = ('qwertyuiop', 'asdfghjkl', 'zxcvbnm')


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


def render_keyboard(statuses: dict[str, str]) -> str:
    rows = []

    for indent, letters in zip((0, 1, 3), KEYBOARD_ROWS):
        keys = []
        for letter in letters:
            colour = statuses.get(letter)
            keys.append(letter.upper() if colour is None
                        else colorize(letter.upper(), COLOUR_CODES[colour]))
        rows.append(' ' * indent + ' '.join(keys))

    return '\n'.join(rows)


def print_board(history: list[tuple[str, list[str]]]) -> None:
    print()
    for guess, colours in history:
        print(render_row(guess, colours))
    print()
    print(render_keyboard(letter_statuses(history)))
    print()


def ordinal(n: int) -> str:
    suffix = 'th' if 11 <= n % 100 <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f'{n}{suffix}'


def letter_statuses(history: list[tuple[str, list[str]]]) -> dict[str, str]:

    statuses: dict[str, str] = {}

    for guess, colours in history:
        for g_letter, colour in zip(guess, colours):
            known = statuses.get(g_letter)
            if known is None or COLOUR_RANK[colour] > COLOUR_RANK[known]:
                statuses[g_letter] = colour

    return statuses


def hard_mode_constraints(
    history: list[tuple[str, list[str]]],
) -> tuple[dict[int, str], Counter]:

    greens: dict[int, str] = {}
    required: Counter = Counter()

    for guess, colours in history:
        revealed = Counter()

        for i, (g_letter, colour) in enumerate(zip(guess, colours)):
            if colour == GREEN:
                greens[i] = g_letter
            if colour in (GREEN, YELLOW):
                revealed[g_letter] += 1

        for letter, count in revealed.items():
            if count > required[letter]:
                required[letter] = count

    return greens, required


def hard_mode_violation(history: list[tuple[str, list[str]]],
                        guess: str) -> str | None:

    greens, required = hard_mode_constraints(history)

    for i, g_letter in enumerate(guess):
        if i in greens and g_letter != greens[i]:
            return (f'Hard mode: {ordinal(i + 1)} letter must be '
                    f'{greens[i].upper()}.')

    counts = Counter(guess)
    for letter, needed in required.items():
        if counts[letter] < needed:
            if needed == 1:
                return f'Hard mode: guess must contain {letter.upper()}.'
            return f"Hard mode: guess must contain {needed} {letter.upper()}'s."

    return None


def play(answers: list[str], accepted: set[str], word_length: int = WORD_LENGTH,
         max_tries: int = MAX_TRIES, hard: bool = HARD_MODE) -> None:
    word = random.choice(answers)
    number_try = 0
    history: list[tuple[str, list[str]]] = []

    while True:
        mode = ' [hard]' if hard else ''
        prompt = (f'Guess {number_try + 1}/{max_tries}{mode} — enter a '
                  f'{word_length} letter word (or q to exit): ')
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

        if hard:
            violation = hard_mode_violation(history, guess)
            if violation:
                print_warning(violation)
                continue

        history.append((guess, score_guess(word, guess)))
        print_board(history)

        if guess == word:
            tries = number_try + 1
            noun = 'try' if tries == 1 else 'tries'
            print_success(f'Congratulations! You guessed the word "{word}" in {tries} {noun}!')
            break

        number_try += 1
        if number_try >= max_tries:
            print(f'You have used all your tries! The word was "{word}".')
            break
