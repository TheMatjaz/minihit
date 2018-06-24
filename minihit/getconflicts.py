#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

import collections
import random

from typing import Generator, Set


class ConflictSetsFileParser(object):
    def __init__(self,
                 comment_char='#',
                 set_separator='|',
                 element_separator=',',
                 element_caster_function=int):
        self.input_file_name = None
        self.comment_char = comment_char
        self.set_separator = set_separator
        self.element_separator = element_separator
        self.element_caster_function = element_caster_function
        self.sets_by_line = collections.OrderedDict()
        self.lines_in_file = 0

    def parse(self, input_file_name):
        self._reset()
        self.input_file_name = input_file_name
        for line in self._clean_lines():
            self.sets_by_line[self.lines_in_file] = self._line_to_sets(line)
        return self.sets_by_line

    def _reset(self):
        self.sets_by_line.clear()
        self.lines_in_file = 0

    def _clean_lines(self):
        with open(self.input_file_name) as input_file:
            for line in input_file:
                self.lines_in_file += 1
                line = self._cleaned_line(line)
                if line:
                    yield line

    def _cleaned_line(self, line):
        no_whitespaces = ''.join(line.split())
        processed = no_whitespaces.split(self.comment_char, 1)[0]
        processed = processed.replace('},{', self.set_separator)
        processed = processed.replace('{', '').replace('}', '')
        processed = processed.replace('[', '').replace(']', '')
        processed = processed.replace('(', '').replace(')', '')
        return processed

    def _line_to_sets(self, line):
        line = line.strip(self.set_separator)
        sets_as_strings = line.split(self.set_separator)
        all_sets = map(self._string_to_set, sets_as_strings)
        filtered_sets = list(filter(None, all_sets))
        return filtered_sets

    def _string_to_set(self, set_as_string):
        set_as_string = set_as_string.strip(self.element_separator)
        elements_as_strings = set_as_string.split(self.element_separator)
        elements_as_strings = filter(None, elements_as_strings)
        elements = map(self.element_caster_function, elements_as_strings)
        elements = set(elements)
        return elements

    def __str__(self):
        strings = []
        for line_number, parsed_set in self.sets_by_line.items():
            strings.append("{:3d}: {:}".format(line_number, parsed_set))
        return '\n'.join(strings)

    def as_set_list(self):
        return list(self.sets_by_line.values())


def random_conflicts(amount_conflicts: int, max_cardinality: int
                     ) -> Generator[Set[int], None, None]:
    """
    Generator of a random sequence of conflicts containing integers.

    Args:
        amount_conflicts: number of conflicts to generate
        max_cardinality: maximum possible size of each conflict in the sequence
            and maximum value that each conflict element can have.

    Returns:
        generator of the conflicts.
    """
    for i in range(amount_conflicts):
        cardinality = random.randint(1, max_cardinality)
        conflict = set(random.randint(1, max_cardinality)
                       for i in range(cardinality))
        yield conflict


def linear_conflicts(amount_conflicts: int, cardinality: int,
                     overlap: int = 1
                     ) -> Generator[Set[int], None, None]:
    """
    Generator of a linear sequence of conflicts containing integers with
    overlapping values between neighbours.

    Args:
        amount_conflicts: number of conflicts to generate
        cardinality: size of each conflict in the sequence
        overlap: amount of values to be overlapping

    Returns:
        generator of the conflicts.
    """
    if overlap > cardinality:
        raise ValueError("Overlap must be smaller than cardinality.")
    if amount_conflicts <= 0 or cardinality <= 0 or overlap <= 0:
        raise ValueError(
            "The linear problem parameters must be strictly positive.")
    previous_last = 1
    for conflict_index in range(amount_conflicts):
        conflict = set(range(previous_last, previous_last + cardinality))
        previous_last += cardinality - overlap
        yield conflict
