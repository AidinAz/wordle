import random
from display import print_success, print_warning, print_gray
from config import WORD_LENGTH


def play(words: list[str], word_length: int = WORD_LENGTH) -> None:
    word = random.choice(words)
    number_try = 0

    while True:
        guess = input(f'Enter a {word_length} letter word (or q to exit): ')

        if guess == 'q':
            break

        if len(guess) != word_length:
            print(f'Word must have {word_length} letters. You entered {len(guess)}!')
            continue

        if guess not in words:
            print_warning(f'Word "{guess}" is not in the list of valid words!')
            continue

        for w_letter, g_letter in zip(word, guess):
            if w_letter == g_letter:
                print_success(g_letter)
            elif g_letter in word:
                print_warning(g_letter)
            else:
                print_gray(g_letter)

        if guess == word:
            print_success(f'Congratulations! You guessed the word "{word}" in {number_try + 1} tries!')
            break

        number_try += 1
        if number_try >= 6:
            print(f'You have used all your tries! The word was "{word}".')
            break
