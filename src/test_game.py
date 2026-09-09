import unittest

from game import score_guess, hard_mode_violation


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
        self.assertEqual(
            score_guess('apple', 'zzzaz'),
            ['gray', 'gray', 'gray', 'yellow', 'gray'],
        )


class TestHardModeViolation(unittest.TestCase):

    def test_empty_history_allows_anything(self):
        self.assertIsNone(hard_mode_violation([], 'crane'))

    def test_green_must_keep_its_position(self):
        history = [('crane', ['gray', 'gray', 'gray', 'gray', 'green'])]
        self.assertEqual(
            hard_mode_violation(history, 'stoat'),
            'Hard mode: 5th letter must be E.',
        )

    def test_guess_keeping_the_green_is_allowed(self):
        history = [('crane', ['gray', 'gray', 'gray', 'gray', 'green'])]
        self.assertIsNone(hard_mode_violation(history, 'shale'))

    def test_yellow_must_be_reused(self):
        history = [('crane', ['gray', 'gray', 'yellow', 'gray', 'gray'])]
        self.assertEqual(
            hard_mode_violation(history, 'toils'),
            'Hard mode: guess must contain A.',
        )

    def test_yellow_may_be_reused_in_the_same_position(self):
        history = [('crane', ['gray', 'gray', 'yellow', 'gray', 'gray'])]
        self.assertIsNone(hard_mode_violation(history, 'plant'))

    def test_gray_letters_may_be_reused(self):
        history = [('crane', ['gray', 'gray', 'yellow', 'gray', 'gray'])]
        self.assertIsNone(hard_mode_violation(history, 'chair'))

    def test_two_revealed_copies_require_two_copies(self):
        history = [('sheep', ['gray', 'gray', 'yellow', 'yellow', 'gray'])]
        self.assertEqual(
            hard_mode_violation(history, 'elbow'),
            "Hard mode: guess must contain 2 E's.",
        )

    def test_two_revealed_copies_satisfied_by_two_copies(self):
        history = [('sheep', ['gray', 'gray', 'yellow', 'yellow', 'gray'])]
        self.assertIsNone(hard_mode_violation(history, 'elite'))

    def test_constraints_persist_across_later_guesses(self):
        history = [
            ('crane', ['gray', 'gray', 'yellow', 'gray', 'gray']),
            ('moist', ['gray', 'gray', 'gray', 'gray', 'gray']),
        ]
        self.assertEqual(
            hard_mode_violation(history, 'blush'),
            'Hard mode: guess must contain A.',
        )

    def test_counts_take_the_max_not_the_sum(self):
        history = [
            ('crane', ['gray', 'gray', 'gray', 'gray', 'yellow']),
            ('elbow', ['yellow', 'gray', 'gray', 'gray', 'gray']),
        ]
        self.assertIsNone(hard_mode_violation(history, 'medal'))


if __name__ == '__main__':
    unittest.main()
