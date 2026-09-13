from config import (DATA_PATH, ANSWERS_PATH, GUESSES_PATH, WORD_LENGTH,
                    ANSWER_LIMIT, MIN_GUESS_FREQUENCY)

CURATED_LENGTH = 5


def read_word_list(path) -> list[str]:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def frequent_words(file_path, word_length, min_frequency) -> list[str]:

    words_frequency = []
    with open(file_path) as f:
        for line in f:
            word, frequency = line.split(', ')
            if len(word) == word_length and int(frequency) >= min_frequency:
                words_frequency.append((word, int(frequency)))

    words_frequency.sort(key=lambda w_freq: w_freq[1], reverse=True)

    return [w for w, _ in words_frequency]


def load_words(file_path=DATA_PATH, word_length=WORD_LENGTH,
               limit=ANSWER_LIMIT, answers_path=ANSWERS_PATH,
               min_frequency=MIN_GUESS_FREQUENCY,
               guesses_path=GUESSES_PATH) -> tuple[list[str], set[str]]:

    curated = word_length == CURATED_LENGTH
    use_answers = curated and answers_path.exists()
    use_guesses = curated and guesses_path.exists()

    frequent = ([] if use_answers and use_guesses
                else frequent_words(file_path, word_length, min_frequency))

    answers = read_word_list(answers_path) if use_answers else frequent[:limit]
    accepted = (set(read_word_list(guesses_path)) if use_guesses
                else set(frequent))

    accepted |= set(answers)

    return answers, accepted
