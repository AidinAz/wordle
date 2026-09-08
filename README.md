# Wordle — Terminal Edition

A command-line clone of the classic [Wordle] word-guessing game, written in Python.

## How to play

Guess a secret 5-letter word in **6 tries**. After each guess the letters are coloured to show how close you were:

| Colour | Meaning |
|--------|---------|
| **Green** | Correct letter, correct position |
| **Yellow** | Letter is in the word, but wrong position |
| **Gray** | Letter is not in the word |

## Requirements

- Python 3.10+

No external dependencies — the standard library is all you need.

## Getting started

```bash
cd src
python run.py
```

Then type a 5-letter word and press Enter. Type `q` to quit at any time.

## Project structure

```
src/
├── run.py       # Entry point
├── config.py    # Word length, guess limit, data path
├── game.py      # Game loop and guess-checking logic
├── display.py   # Coloured terminal output helpers
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
| `MIN_GUESS_FREQUENCY` | `50000` | Minimum corpus frequency for a word to be accepted as a guess — filters scanner noise out of the 333 k-word list |
| `DATA_PATH` | `data/words.txt` | Path to the word frequency list |
| `ANSWERS_PATH` | `data/answers.txt` | Path to the curated 5-letter answer list |

At the default `WORD_LENGTH` of 5 the secret is drawn from `answers.txt`, a curated list of 2 309 common words — so you'll never be asked to guess a proper noun or an abbreviation. Any other word length falls back to the `ANSWER_LIMIT` most frequent words of that length, which is a noticeably rougher pool.

The answer pool only restricts the *secret*. A guess just has to be the right length and clear the `MIN_GUESS_FREQUENCY` floor, so you can play far more words than can ever be the answer — about 17 700 at the default 5 letters. The floor exists because `words.txt` is a raw frequency corpus whose long tail is scanner noise (`gvole`, `gpoge`, `goolh`); without it roughly 28 000 of those non-words would be accepted as legitimate guesses. Every curated answer stays guessable regardless of its frequency.
