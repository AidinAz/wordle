import unittest

from game import score_guess


class TestScoreGuess(unittest.TestCase):

    def test_exact_match(self):
        self.assertEqual(
            score_guess('apple', 'apple'),
            ['green', 'green', 'green', 'green', 'green'],
        )

    def test_no_overlap(self):
        self.assertEqual(
            score_guess('apple', 'north'),
            ['gray', 'gray', 'gray', 'gray', 'gray'],
        )

    def test_simple_yellow(self):
        self.assertEqual(
            score_guess('apple', 'lemon'),
            ['yellow', 'yellow', 'gray', 'gray', 'gray'],
        )

    def test_repeated_guess_letter_single_occurrence_in_word(self):
        # Only one 'p' should score, the rest stay gray even though the
        # word has two 'p's total (both consumed as greens already).
        self.assertEqual(
            score_guess('apple', 'ppppp'),
            ['gray', 'green', 'green', 'gray', 'gray'],
        )

    def test_repeated_letter_in_both_word_and_guess(self):
        self.assertEqual(
            score_guess('sheep', 'epees'),
            ['gray', 'yellow', 'green', 'green', 'yellow'],
        )

    def test_repeated_guess_letter_absent_from_word(self):
        # 'z' doesn't appear in the word at all, so both instances stay gray.
        self.assertEqual(
            score_guess('apple', 'zzzaz'),
            ['gray', 'gray', 'gray', 'yellow', 'gray'],
        )


if __name__ == '__main__':
    unittest.main()
