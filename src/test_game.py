import contextlib
import io
import unittest
from unittest import mock

import display
from display import GREEN_FG
from game import (score_guess, hard_mode_violation, letter_statuses,
                  validate_guess, render_row, render_keyboard, render_blank_row,
                  render_frame, play)


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


class TestLetterStatuses(unittest.TestCase):

    def test_empty_history_knows_nothing(self):
        self.assertEqual(letter_statuses([]), {})

    def test_single_guess_records_each_letter(self):
        history = [('crane', ['gray', 'gray', 'yellow', 'gray', 'green'])]
        self.assertEqual(
            letter_statuses(history),
            {'c': 'gray', 'r': 'gray', 'a': 'yellow', 'n': 'gray', 'e': 'green'},
        )

    def test_untried_letters_are_absent(self):
        history = [('crane', ['gray', 'gray', 'gray', 'gray', 'gray'])]
        self.assertNotIn('z', letter_statuses(history))

    def test_gray_then_green_upgrades(self):
        history = [
            ('toils', ['gray', 'gray', 'gray', 'gray', 'gray']),
            ('stoat', ['gray', 'gray', 'gray', 'gray', 'green']),
        ]
        self.assertEqual(letter_statuses(history)['t'], 'green')

    def test_green_is_never_downgraded_by_a_later_gray(self):
        history = [
            ('stoat', ['gray', 'gray', 'gray', 'gray', 'green']),
            ('toils', ['gray', 'gray', 'gray', 'gray', 'gray']),
        ]
        self.assertEqual(letter_statuses(history)['t'], 'green')

    def test_yellow_then_green_upgrades(self):
        history = [
            ('crane', ['gray', 'gray', 'yellow', 'gray', 'gray']),
            ('plant', ['gray', 'gray', 'green', 'gray', 'gray']),
        ]
        self.assertEqual(letter_statuses(history)['a'], 'green')

    def test_yellow_is_never_downgraded_by_a_later_gray(self):
        history = [
            ('crane', ['gray', 'gray', 'yellow', 'gray', 'gray']),
            ('plant', ['gray', 'gray', 'gray', 'gray', 'gray']),
        ]
        self.assertEqual(letter_statuses(history)['a'], 'yellow')

    def test_duplicate_letter_yellow_beats_gray_within_one_guess(self):
        history = [('sheep', score_guess('elbow', 'sheep'))]
        self.assertEqual(letter_statuses(history)['e'], 'yellow')

    def test_duplicate_letter_green_beats_gray_within_one_guess(self):
        history = [('ppppp', score_guess('apple', 'ppppp'))]
        self.assertEqual(letter_statuses(history)['p'], 'green')


class TestValidateGuess(unittest.TestCase):

    ACCEPTED = {'crane', 'slate', 'plant'}

    def test_wrong_length(self):
        message = validate_guess('cat', self.ACCEPTED, [])
        self.assertEqual(message,
                         'Word must have 5 letters. You entered 3!')

    def test_not_in_word_list(self):
        message = validate_guess('zzzzz', self.ACCEPTED, [])
        self.assertIn('not in the list of valid words', message)

    def test_legal_guess_passes(self):
        self.assertIsNone(validate_guess('crane', self.ACCEPTED, []))

    def test_repeated_guess_is_rejected(self):
        history = [('crane', score_guess('slate', 'crane'))]
        message = validate_guess('crane', self.ACCEPTED, history)
        self.assertEqual(message, 'You already guessed "crane". Try a new word!')

    def test_repeat_is_rejected_outside_hard_mode(self):
        history = [('crane', score_guess('slate', 'crane'))]
        self.assertIsNotNone(
            validate_guess('crane', self.ACCEPTED, history, hard=False))

    def test_repeat_message_wins_over_hard_mode_violation(self):
        history = [('plant', score_guess('crane', 'plant'))]
        message = validate_guess('plant', self.ACCEPTED, history, hard=True)
        self.assertIn('already guessed', message)

    def test_a_rejected_guess_is_not_a_repeat(self):
        self.assertIsNone(validate_guess('crane', self.ACCEPTED, []))


class DisplayModeMixin:

    COLOUR = False
    SCREEN = False

    def setUp(self):
        self._saved = (display._COLOUR, display._SCREEN)
        display._COLOUR, display._SCREEN = self.COLOUR, self.SCREEN

    def tearDown(self):
        display._COLOUR, display._SCREEN = self._saved


class TestPlainRendering(DisplayModeMixin, unittest.TestCase):

    def test_row_uses_the_glyph_legend(self):
        self.assertEqual(render_row('crane', score_guess('slate', 'crane')),
                         ' c   r  [A]  n  [E]')

    def test_yellow_uses_parentheses(self):
        self.assertEqual(render_row('least', score_guess('slate', 'least')),
                         '(L) (E) [A] (S) (T)')

    def test_row_has_no_escape_codes(self):
        row = render_row('crane', score_guess('slate', 'crane'))
        self.assertNotIn('\033', row)

    def test_keyboard_has_no_escape_codes(self):
        keyboard = render_keyboard(letter_statuses(
            [('crane', score_guess('slate', 'crane'))]))
        self.assertNotIn('\033', keyboard)

    def test_rows_align_regardless_of_score(self):
        widths = {len(render_row(guess, score_guess('slate', guess)))
                  for guess in ('crane', 'least', 'slate', 'plant')}
        self.assertEqual(widths, {19})

    def test_keyboard_indents_scale_with_cell_pitch(self):
        rows = render_keyboard({}).split('\n')
        self.assertEqual([len(r) - len(r.lstrip(' ')) for r in rows], [1, 3, 7])

    def test_untried_key_differs_from_ruled_out_key(self):
        statuses = letter_statuses([('crane', score_guess('slate', 'crane'))])
        keyboard = render_keyboard(statuses)
        self.assertIn(' c ', keyboard)
        self.assertIn(' Z ', keyboard)


class TestColourRendering(DisplayModeMixin, unittest.TestCase):

    COLOUR = True
    SCREEN = True

    def test_row_still_uses_ansi_colour(self):
        row = render_row('crane', score_guess('slate', 'crane'))
        self.assertIn(GREEN_FG, row)

    def test_row_format_is_unchanged(self):
        from display import colorize, GRAY_FG
        expected = ' '.join([
            colorize('C', GRAY_FG), colorize('R', GRAY_FG),
            colorize('A', GREEN_FG), colorize('N', GRAY_FG),
            colorize('E', GREEN_FG),
        ])
        self.assertEqual(render_row('crane', score_guess('slate', 'crane')),
                         expected)


class TestRenderFrameAppendMode(DisplayModeMixin, unittest.TestCase):

    def test_only_the_newest_row_is_emitted(self):
        history = [('crane', score_guess('slate', 'crane')),
                   ('plant', score_guess('slate', 'plant'))]
        frame = render_frame(history)
        self.assertIn(render_row('plant', history[1][1]), frame)
        self.assertNotIn(render_row('crane', history[0][1]), frame)

    def test_a_message_is_emitted_alone(self):
        history = [('crane', score_guess('slate', 'crane'))]
        frame = render_frame(history, 'Nope!')
        self.assertEqual(frame, 'Nope!')

    def test_empty_history_renders_nothing(self):
        self.assertEqual(render_frame([]), '')


class TestRenderFrameScreenMode(DisplayModeMixin, unittest.TestCase):

    SCREEN = True

    def test_placeholders_pad_the_board_to_max_tries(self):
        history = [('crane', score_guess('slate', 'crane'))]
        frame = render_frame(history, max_tries=6)
        self.assertEqual(frame.count(render_blank_row()), 5)

    def test_every_row_is_kept_not_just_the_newest(self):
        history = [('crane', score_guess('slate', 'crane')),
                   ('plant', score_guess('slate', 'plant'))]
        frame = render_frame(history)
        self.assertIn(render_row('crane', history[0][1]), frame)
        self.assertIn(render_row('plant', history[1][1]), frame)

    def test_frame_height_is_constant_with_and_without_a_message(self):
        history = [('crane', score_guess('slate', 'crane'))]
        quiet = render_frame(history).count('\n')
        noisy = render_frame(history, 'Nope!').count('\n')
        self.assertEqual(quiet, noisy)


class TestPlayLoop(DisplayModeMixin, unittest.TestCase):

    def run_game(self, word, guesses, accepted, max_tries=6):
        out = io.StringIO()
        with mock.patch('random.choice', return_value=word), \
             mock.patch('builtins.input', side_effect=guesses), \
             contextlib.redirect_stdout(out):
            play([word], accepted, max_tries=max_tries)
        return out.getvalue()

    def test_repeated_guess_does_not_burn_a_try(self):
        output = self.run_game('slate', ['crane', 'crane', 'slate'],
                               {'slate', 'crane'})
        self.assertIn('already guessed', output)
        self.assertIn('in 2 tries', output)

    def test_invalid_guess_does_not_burn_a_try(self):
        output = self.run_game('slate', ['zzzzz', 'cat', 'slate'], {'slate'})
        self.assertIn('in 1 try', output)

    def test_plain_output_has_no_escape_codes(self):
        output = self.run_game('slate', ['crane', 'plant', 'slate'],
                               {'slate', 'crane', 'plant'})
        self.assertNotIn('\033', output)

    def test_each_row_is_printed_exactly_once(self):
        output = self.run_game('slate', ['crane', 'plant', 'slate'],
                               {'slate', 'crane', 'plant'})
        row = render_row('crane', score_guess('slate', 'crane'))
        self.assertEqual(output.count(row), 1)

    def test_loss_reveals_the_word(self):
        output = self.run_game('slate', ['crane', 'plant'],
                               {'crane', 'plant'}, max_tries=2)
        self.assertIn('used all your tries', output)
        self.assertIn('slate', output)


if __name__ == '__main__':
    unittest.main()
