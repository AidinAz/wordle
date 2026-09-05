import random
from collections import Counter
from display import print_success, print_warning, print_gray
from config import WORD_LENGTH, MAX_TRIES

GREEN, YELLOW, GRAY = 'green', 'yellow', 'gray'


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


def play(answers: list[str], accepted: set[str], word_length: int = WORD_LENGTH,
         max_tries: int = MAX_TRIES) -> None:
    word = random.choice(answers)
    number_try = 0

    while True:
        guess = input(f'Enter a {word_length} letter word (or q to exit): ').strip().lower()

        if guess == 'q':
            break

        if len(guess) != word_length:
            print_warning(f'Word must have {word_length} letters. You entered {len(guess)}!')
            continue

        if guess not in accepted:
            print_warning(f'Word "{guess}" is not in the list of valid words!')
            continue

        for g_letter, colour in zip(guess, score_guess(word, guess)):
            if colour == GREEN:
                print_success(g_letter)
            elif colour == YELLOW:
                print_warning(g_letter)
            else:
                print_gray(g_letter)

        if guess == word:
            print_success(f'Congratulations! You guessed the word "{word}" in {number_try + 1} tries!')
            break

        number_try += 1
        if number_try >= max_tries:
            print(f'You have used all your tries! The word was "{word}".')
            break
