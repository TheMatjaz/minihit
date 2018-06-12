#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from unittest import TestCase

from minihit.fileload import ConflictSetsFileParser


class TestConflictSetsFileParser(TestCase):
    def setUp(self):
        self.input_files_folder = 'parser_files'
        self.files_and_expected = {
            '01_empty.txt': {},
            '02_only_comments.txt': {},
            '03_simple_one_line.txt': {1: [{1, 2}, {3, 4}, {1, 2, 5}]},
            '04_redundant_values_in_first_set.txt': {1: [{1}, {3, 4}]},
            '05_trailing_commas.txt': {1: [{1}, {1, 2}]},
            '06_empty_last_set.txt': {1: [{1, 2}, {2, 3}]},
            '07_empty_first_set.txt': {1: [{1, 2}]},
            '08_empty_middle_set.txt': {1: [{1, 2}, {3, 4}]},
            '09_simple_multiline.txt': {
                1: [{1, 2}, {3, 4}, {1, 2, 5}],
                2: [{2, 3}, {4, 5}, {1, 2, 5}]
            },
            '10_simple_multiline_with_comments.txt': {
                1: [{1, 2}, {3, 4}, {1, 2, 5}],
                3: [{2, 3}, {4, 5}, {1, 2, 5}]
            },
            '11_combined.txt': {
                2: [{1, 2}, {3, 4}, {1, 2, 5}],
                3: [{1}, {3, 4}],
                4: [{1}, {1, 2}],
                5: [{1, 2}, {2, 3}],
                6: [{1, 2}],
                7: [{1, 2}, {3, 4}],
            },
            '12_with_brackets.txt': {
                1: [{1, 2}, {3, 4}, {1, 2, 5}],
                2: [{2, 3}, {4, 5}, {1, 2, 5}]
            },
        }

    def test_all(self):
        for file_name, expected in self.files_and_expected.items():
            relative_file_path = os.path.join(self.input_files_folder,
                                              file_name)
            parser = ConflictSetsFileParser()
            result = parser.parse(relative_file_path)
            self.assertDictEqual(expected, result, file_name)
