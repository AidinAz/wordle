from config import DATA_PATH, WORD_LENGTH, LIMIT


def load_words(file_path=DATA_PATH, word_length=WORD_LENGTH, limit=LIMIT) -> list[str]:
    words_frequency = []
    with open(file_path) as f:
        for line in f:
            word, frequency = line.split(', ')
            words_frequency.append((word, int(frequency)))

    words_frequency.sort(key=lambda w_freq: w_freq[1], reverse=True)
    words_frequency = words_frequency[:limit]

    return [w for w, _ in words_frequency if len(w) == word_length]
