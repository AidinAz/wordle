# Wordle — Terminal Edition

A command-line clone of the classic [Wordle](https://www.nytimes.com/games/wordle/index.html) word-guessing game, written in Python.

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
├── words.py     # Word list loader (filters by length and frequency)
└── data/
    └── words.txt  # ~333 k words with frequency scores
```

## Configuration

Edit [src/config.py](src/config.py) to tweak the game:

| Variable | Default | Description |
|----------|---------|-------------|
| `WORD_LENGTH` | `5` | Number of letters in the secret word |
| `LIMIT` | `1000` | Only the top-N most frequent words are used |
| `DATA_PATH` | `data/words.txt` | Path to the word frequency list |

Increasing `LIMIT` makes the game harder (rarer words can be chosen); decreasing it keeps answers common and familiar.
