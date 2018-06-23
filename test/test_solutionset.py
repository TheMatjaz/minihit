#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from minihit.mhs import SolutionSet


class TestSolutionSet(TestCase):
    def setUp(self):
        self.list_of_conflicts = [{1, 2}, {3, 4}, {1, 2, 5}]

    def test_empty_is_not_hitting(self):
        solution_set = SolutionSet()
        self.assertFalse(solution_set.is_hitting(self.list_of_conflicts))

    def test_is_hitting_when_hitting(self):
        solution_set = SolutionSet([1, 2, 3])
        self.assertTrue(solution_set.is_hitting(self.list_of_conflicts))

    def test_is_not_hitting_when_not_hitting(self):
        solution_set = SolutionSet([99])
        self.assertFalse(solution_set.is_hitting(self.list_of_conflicts))

    def test_empty_is_not_minimal_hitting(self):
        solution_set = SolutionSet()
        self.assertFalse(
            solution_set.is_minimal_hitting(self.list_of_conflicts))

    def test_is_minimal_hitting_when_minimal_hitting(self):
        solution_set = SolutionSet([1, 3])
        self.assertTrue(solution_set.is_minimal_hitting(self.list_of_conflicts))

    def test_is_not_minimal_hitting_when_not_hitting(self):
        solution_set = SolutionSet([99])
        self.assertFalse(
            solution_set.is_minimal_hitting(self.list_of_conflicts))

    def test_is_not_minimal_hitting_when_not_minimal(self):
        solution_set = SolutionSet([1, 2, 3, 4, 5, 6, 7])
        self.assertFalse(
            solution_set.is_minimal_hitting(self.list_of_conflicts))

    def test_is_minimal_hitting_when_minimal_with_single_element_conflict_set(
            self):
        solution_set = SolutionSet([1, 3])
        self.assertTrue(solution_set.is_minimal_hitting([{1}, {1, 3, 4}]))

    def test_equality_between_solutionsets(self):
        solution_set_1 = SolutionSet()
        solution_set_2 = SolutionSet()
        self.assertEqual(solution_set_1, solution_set_2)
        solution_set_1 = SolutionSet([1, 2])
        solution_set_2 = SolutionSet([1, 2])
        self.assertEqual(solution_set_1, solution_set_2)

    def test_equality_between_solutionset_and_set(self):
        solution_set_1 = SolutionSet()
        set_2 = set()
        self.assertEqual(solution_set_1, set_2)
        solution_set_1 = SolutionSet([1, 2])
        set_2 = {1, 2}
        self.assertEqual(solution_set_1, set_2)
