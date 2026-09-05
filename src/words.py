from config import DATA_PATH, WORD_LENGTH, ANSWER_LIMIT


def load_words(file_path=DATA_PATH, word_length=WORD_LENGTH,
               limit=ANSWER_LIMIT) -> tuple[list[str], set[str]]:
    
    words_frequency = []
    with open(file_path) as f:
        for line in f:
            word, frequency = line.split(', ')
            if len(word) == word_length:
                words_frequency.append((word, int(frequency)))

    words_frequency.sort(key=lambda w_freq: w_freq[1], reverse=True)

    accepted = {w for w, _ in words_frequency}
    answers = [w for w, _ in words_frequency[:limit]]

    return answers, accepted
