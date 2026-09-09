from pathlib import Path

WORD_LENGTH = 5
ANSWER_LIMIT = 2000
MAX_TRIES = 6
HARD_MODE = False
MIN_GUESS_FREQUENCY = 50_000
DATA_PATH = Path(__file__).parent / "data" / "words.txt"
ANSWERS_PATH = Path(__file__).parent / "data" / "answers.txt"
