import hashlib
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath('../src'))

from textcut import TextCut

text = ("Lorem ipsum dolores sit amet aliquam id diam maecenas ultricies mi eget " +
        "mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis " +
        "eleifend quam adipiscing vitae proin sagittis nisl rhoncus mattis rhoncus " +
        "urna neque viverra justo nec ultrices dui sapien eget mi proin sed libero " +
        "enim sed faucibus turpis in eu.\n\nMi bibendum neque egestas congue quisque " +
        "egestas diam in arcu cursus euismod quis viverra nibh cras pulvinar mattis " +
        "nunc sed blandit libero volutpat sed cras ornare arcu dui vivamus arcu felis " +
        "bibendum ut tristique et egestas quis ipsum suspendisse ultrices gravida " +
        "dictum fusce ut placerat orci nulla pellentesque dignissim enim sit amet " +
        "venenatis urna cursus eget nunc scelerisque viverra mauris in aliquam sem " +
        "fringilla ut morbi tincidunt augue interdum velit euismod in pellentesque massa " +
        "placerat duis ultricies lacus sed turpis tincidunt id aliquet risus feugiat in " +
        "ante metus dictum at tempor commodo ullamcorper a lacus vestibulum sed arcu " +
        "non odio.\n\nEuismod lacinia at quis risus sed vulputate odio ut enim blandit " +
        "volutpat maecenas volutpat blandit aliquam etiam erat velit scelerisque in dictum " +
        "non consectetur a erat nam at lectus urna duis convallis convallis tellus id " +
        "interdum velit laoreet id donec ultrices tincidunt arcu non sodales neque " +
        "sodales ut etiam sit")

class TestTextCut(unittest.TestCase):

    def test_wrap_default(self):
        self.assertEqual(
                [99, 98, 96, 31, 99, 92, 97, 99, 95, 95, 74, 99, 93, 97, 26],
                [len(x) for x in TextCut().wrap(text)])

    def test_wrap_small_width(self):
        self.assertEqual(
                [5, 5, 7, 8, 7, 7, 8, 9, 7, 6, 8, 2, 8, 5, 6, 6, 7, 9, 9,
                 8, 4, 10, 5, 5, 8, 4, 7, 6, 7, 4, 5, 7, 9, 8, 3, 6, 7, 9,
                 6, 8, 8, 9, 3, 2, 8, 5, 7, 6, 7, 7, 7, 4, 6, 7, 4, 7, 9,
                 8, 6, 8, 7, 6, 8, 8, 6, 8, 7, 4, 5, 8, 2, 9, 2, 7, 4, 5,
                 10, 10, 7, 6, 8, 8, 4, 5, 10, 2, 9, 8, 4, 9, 4, 6, 9, 10,
                 9, 9, 7, 3, 9, 8, 9, 5, 8, 5, 7, 2, 10, 8, 8, 4, 9, 9, 6,
                 9, 2, 7, 5, 7, 7, 5, 9, 6, 7, 10, 9, 10, 8, 9, 7, 7, 7,
                 9, 9, 7, 4, 7, 8, 8, 8, 7, 7, 5, 4, 5, 10, 4, 6, 3, 10,
                 8, 6, 6, 9, 9, 9, 9, 8, 5, 7, 8, 8, 9, 8, 7, 5, 7, 8, 3],
                [len(x) for x in TextCut(width = 10).wrap(text)])

    def test_wrap_big_width(self):
        self.assertEqual(
                [327, 492, 484],
                [len(x) for x in TextCut(width = 500).wrap(text)])

    def test_wrap_huge_width(self):
        self.assertEqual(
                [1306],
                [len(x) for x in TextCut(width = 10000).wrap(text)])

    def test_wrap_zero_width(self):
        with self.assertRaises(ValueError):
            TextCut(width = 0).wrap(text)

    def test_wrap_empty_string(self):
        self.assertEqual(
                [''], TextCut().wrap(''))

    def test_wrap_untrimmed(self):
        self.assertEqual(
                [100, 99, 97, 33, 100, 93, 98, 100, 96, 96, 76, 100, 94, 98, 26],
                [len(x) for x in TextCut(trim = False).wrap(text)])

    def test_wrap_non_linear_length(self):
        self.assertEqual(
                [99, 98, 101, 26, 99, 101, 99, 98, 100, 97, 57, 99, 103, 114],
                [len(x) for x in TextCut(len_func = lambda x: sum([1 for c in x if c != " "])).wrap(text)])

    def test_wrap_small_tolerance(self):
        self.assertEqual(
                [99, 98, 100, 98, 100, 99, 100, 100, 99, 100, 100, 100, 98, 9],
                [len(x) for x in TextCut(tolerance = 0.01).wrap(text)])

    def test_wrap_big_tolerance(self):
        self.assertEqual(
                [99, 98, 96, 31, 99, 92, 97, 99, 95, 95, 74, 99, 93, 97, 26],
                [len(x) for x in TextCut(tolerance = 100).wrap(text)])

    def test_fill_default(self):
        h = hashlib.new('sha256')
        h.update(TextCut().fill(text).encode())
        self.assertEqual(
                "25de25b02086947eebeba4a46def91c825f8e887e84472dc687958e9be249a83",
                h.hexdigest())


if __name__ == "__main__":
    unittest.main()
