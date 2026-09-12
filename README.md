# Wordle — Terminal Edition

A command-line clone of the classic [Wordle] word-guessing game, written in Python.

## How to play

Guess a secret 5-letter word in **6 tries**. After each guess the letters are coloured to show how close you were:

| Colour | Plain text | Meaning |
|--------|------------|---------|
| **Green** | `[A]` | Correct letter, correct position |
| **Yellow** | `(A)` | Letter is in the word, but wrong position |
| **Gray** | ` a ` | Letter is not in the word |

The plain-text column is what you get when colour is switched off — see [Colour and output](#colour-and-output).

## Requirements

- Python 3.10+

No external dependencies — the standard library is all you need.

## Getting started

```bash
cd src
python run.py
```

Then type a 5-letter word and press Enter. Type `q` to quit at any time.

When a game ends, you're asked whether to play again. Press Enter or type `y` for a new word, or `n` to stop. The word list is loaded only once, so the next round starts right away.

The board is redrawn in place after every guess, and a keyboard underneath tracks which letters are still in play. Repeating a word you've already guessed is refused for free, so a slip of the memory never costs you a turn.

## Colour and output

The game adapts to where its output is going:

| Situation | Behaviour |
|-----------|-----------|
| A terminal | Colour, redrawn in place |
| `NO_COLOR=1` | Plain-text glyphs, still redrawn in place |
| Piped or redirected | Plain text, appended as a transcript — no escape codes |
| `FORCE_COLOR=1` | Keeps colour through a pipe, for `less -R` and friends |
| `TERM=dumb` | Plain text, no redrawing |

Colour and redrawing are decided separately: [`NO_COLOR`](https://no-color.org) means "don't colour", not "don't redraw", so an accessible session still gets the in-place board. When the screen isn't ours, each guess is appended as a single row instead of reprinting the whole board, which keeps a piped transcript readable.

## Hard mode

```bash
python run.py --hard
```

Hard mode makes every hint binding — you can no longer throw away a turn on a word that ignores what you've already learned:

- A **green** letter is locked to its position and must stay there in every later guess.
- A **yellow** letter must appear somewhere in every later guess, though *not* necessarily in a new spot — leaving it where it was rejected is allowed.
- **Gray** letters are still fair game. Real Wordle never blocks a letter you've ruled out, and neither does this.

Guesses that break a rule are rejected with an explanation and **don't cost you a try**, exactly like a misspelling, a repeat, or a word of the wrong length.

If you've made hard mode the default by setting `HARD_MODE = True` in [src/config.py](src/config.py), `--no-hard` turns it back off for a single game:

```bash
python run.py --no-hard
```

## Project structure

```
src/
├── run.py       # Entry point and CLI flags
├── config.py    # Word length, guess limit, data path
├── game.py      # Game loop, guess-checking, rendering, and hard-mode rules
├── display.py   # Colour/TTY detection, screen control, output helpers
├── words.py     # Word list loader (answer pool + accepted guesses)
└── data/
    ├── words.txt    # ~333 k words with frequency scores (accepted guesses)
    └── answers.txt  # 2 309 curated 5-letter answers
```

## Configuration

Edit [src/config.py](src/config.py) to tweak the game:

| Variable | Default | Description |
|----------|---------|-------------|
| `WORD_LENGTH` | `5` | Number of letters in the secret word |
| `ANSWER_LIMIT` | `2000` | Size of the fallback answer pool — only used when `WORD_LENGTH` is not 5 |
| `MAX_TRIES` | `6` | Number of guesses allowed |
| `HARD_MODE` | `False` | Require every revealed hint to be reused — set it here to make hard mode the default, or override it per game with `--hard` / `--no-hard` |
| `MIN_GUESS_FREQUENCY` | `50000` | Minimum corpus frequency for a word to be accepted as a guess — filters scanner noise out of the 333 k-word list |
| `DATA_PATH` | `data/words.txt` | Path to the word frequency list |
| `ANSWERS_PATH` | `data/answers.txt` | Path to the curated 5-letter answer list |

At the default `WORD_LENGTH` of 5 the secret is drawn from `answers.txt`, a curated list of 2 309 common words — so you'll never be asked to guess a proper noun or an abbreviation. Any other word length falls back to the `ANSWER_LIMIT` most frequent words of that length, which is a noticeably rougher pool.

The answer pool only restricts the *secret*. A guess just has to be the right length and clear the `MIN_GUESS_FREQUENCY` floor, so you can play far more words than can ever be the answer — about 17 700 at the default 5 letters. The floor exists because `words.txt` is a raw frequency corpus whose long tail is scanner noise (`gvole`, `gpoge`, `goolh`); without it roughly 28 000 of those non-words would be accepted as legitimate guesses. Every curated answer stays guessable regardless of its frequency.
