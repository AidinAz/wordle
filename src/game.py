import random
from collections import Counter
from display import (colorize, clear_sequence, print_success, use_colour,
                     use_screen_control, GREEN_FG, YELLOW_FG, GRAY_FG)
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


def render_cell(letter: str, colour: str | None) -> str:
    """One board or keyboard cell: 1 char wide in colour, 3 chars in plain text."""
    if use_colour():
        return (letter.upper() if colour is None
                else colorize(letter.upper(), COLOUR_CODES[colour]))

    if colour == GREEN:
        return f'[{letter.upper()}]'
    if colour == YELLOW:
        return f'({letter.upper()})'
    if colour == GRAY:
        return f' {letter.lower()} '  # ruled out
    return f' {letter.upper()} '      # untried


def render_row(guess: str, colours: list[str]) -> str:
    return ' '.join(render_cell(g_letter, colour)
                    for g_letter, colour in zip(guess, colours))


def render_blank_row(word_length: int = WORD_LENGTH) -> str:
    slot = '_' if use_colour() else ' _ '
    return colorize(' '.join([slot] * word_length), GRAY_FG)


def render_keyboard(statuses: dict[str, str]) -> str:
    unit = 1 if use_colour() else 2
    rows = []

    for indent, letters in zip((0, 1, 3), KEYBOARD_ROWS):
        keys = ' '.join(render_cell(letter, statuses.get(letter))
                        for letter in letters)
        rows.append(' ' * (indent * unit) + keys)

    return '\n'.join(rows)


def render_frame(history: list[tuple[str, list[str]]], message: str | None = None,
                 word_length: int = WORD_LENGTH,
                 max_tries: int = MAX_TRIES) -> str:
    lines: list[str] = []

    if use_screen_control():
        lines.append('')
        lines.extend(render_row(guess, colours) for guess, colours in history)
        lines.extend([render_blank_row(word_length)] * (max_tries - len(history)))
        lines.append('')
        lines.append(render_keyboard(letter_statuses(history)))
        lines.append('')
        # Always reserve the message line so the prompt never jumps.
        lines.append(colorize(message, YELLOW_FG) if message else '')
    elif message:
        lines.append(colorize(message, YELLOW_FG))
    elif history:
        guess, colours = history[-1]
        lines.extend(['', render_row(guess, colours), '',
                      render_keyboard(letter_statuses(history)), ''])

    return '\n'.join(lines)


def draw_frame(history: list[tuple[str, list[str]]], message: str | None = None,
               word_length: int = WORD_LENGTH,
               max_tries: int = MAX_TRIES) -> None:
    frame = clear_sequence() + render_frame(history, message, word_length, max_tries)
    if frame:
        print(frame)


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


def validate_guess(guess: str, accepted: set[str],
                   history: list[tuple[str, list[str]]],
                   word_length: int = WORD_LENGTH,
                   hard: bool = HARD_MODE) -> str | None:

    if len(guess) != word_length:
        return f'Word must have {word_length} letters. You entered {len(guess)}!'

    if guess not in accepted:
        return f'Word "{guess}" is not in the list of valid words!'

    if any(guess == previous for previous, _ in history):
        return f'You already guessed "{guess}". Try a new word!'

    if hard:
        return hard_mode_violation(history, guess)

    return None


def play(answers: list[str], accepted: set[str], word_length: int = WORD_LENGTH,
         max_tries: int = MAX_TRIES, hard: bool = HARD_MODE) -> None:
    word = random.choice(answers)
    history: list[tuple[str, list[str]]] = []
    message: str | None = None

    while True:
        draw_frame(history, message, word_length, max_tries)
        message = None

        mode = ' [hard]' if hard else ''
        prompt = (f'Guess {len(history) + 1}/{max_tries}{mode} — enter a '
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

        message = validate_guess(guess, accepted, history, word_length, hard)
        if message:
            continue  # no try consumed

        history.append((guess, score_guess(word, guess)))
        solved = guess == word

        if solved or len(history) >= max_tries:
            draw_frame(history, None, word_length, max_tries)
            if solved:
                tries = len(history)
                noun = 'try' if tries == 1 else 'tries'
                print_success(f'Congratulations! You guessed the word "{word}" '
                              f'in {tries} {noun}!')
            else:
                print(f'You have used all your tries! The word was "{word}".')
            break
