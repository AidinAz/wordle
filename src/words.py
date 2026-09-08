from config import (DATA_PATH, ANSWERS_PATH, WORD_LENGTH, ANSWER_LIMIT,
                    MIN_GUESS_FREQUENCY)

CURATED_LENGTH = 5


def load_words(file_path=DATA_PATH, word_length=WORD_LENGTH,
               limit=ANSWER_LIMIT, answers_path=ANSWERS_PATH,
               min_frequency=MIN_GUESS_FREQUENCY) -> tuple[list[str], set[str]]:

    words_frequency = []
    with open(file_path) as f:
        for line in f:
            word, frequency = line.split(', ')
            if len(word) == word_length and int(frequency) >= min_frequency:
                words_frequency.append((word, int(frequency)))

    words_frequency.sort(key=lambda w_freq: w_freq[1], reverse=True)

    accepted = {w for w, _ in words_frequency}

    if word_length == CURATED_LENGTH and answers_path.exists():
        with open(answers_path) as f:
            answers = [line.strip() for line in f if line.strip()]
    else:
        answers = [w for w, _ in words_frequency[:limit]]

    accepted |= set(answers)

    return answers, accepted
