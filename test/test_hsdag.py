#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import TestCase

from minihit.hsdag import HsDag, HsDagNode


class TestHsDagNode(TestCase):
    def test_default_constructor(self):
        node = HsDagNode()
        self.assertFalse(node.is_ticked)
        self.assertFalse(node.is_closed)
        self.assertEqual(0, len(node.path_from_root))
        self.assertEqual(0, len(node.parents))
        self.assertEqual(0, len(node.children))
        self.assertIsNone(node.label)

    def test_closing(self):
        node = HsDagNode()
        self.assertFalse(node.is_closed)
        node.close()
        self.assertTrue(node.is_closed)

    def test_ticking(self):
        node = HsDagNode()
        self.assertFalse(node.is_ticked)
        node.tick()
        self.assertTrue(node.is_ticked)

    def test_ticking_removes_label(self):
        node = HsDagNode()
        self.assertFalse(node.is_ticked)
        node.label = {1, 2, 3}
        node.tick()
        self.assertIsNone(node.label)

    def test_cannot_relabel_already_ticked(self):
        node = HsDagNode()
        node.tick()
        with self.assertRaises(ValueError):
            node.label = {667, 987564}

    def test_can_relabel_non_ticked(self):
        node = HsDagNode()
        node.label = {1, 2, 3}
        self.assertEqual({1, 2, 3}, node.label)
        node.label = {9}
        self.assertEqual({9}, node.label)


class TestHsDag(TestCase):
    def setUp(self):
        self.solve_options = [
            (False, False),
            (False, True),
            (True, False),
            (True, True),
        ]

    def test_empty_conflict_sets_does_nothing(self):
        hs_dag = HsDag([])
        for solve_args in self.solve_options:
            elapsed = hs_dag.solve(*solve_args)
            self.assertEqual(0, len(hs_dag.nodes))
            self.assertEqual([], list(hs_dag.generate_minimal_hitting_sets()))
            self.assertIsNone(hs_dag.root)
            self.assertTrue(elapsed < 0.5)
            self.assertTrue(hs_dag.verify())

    def test_solving_minimal_sorted_conflict_sets_1(self):
        conflict_sets = [{1, 3}, {1, 4}]
        expected_mhs = [{1}, {3, 4}]
        hs_dag = HsDag(conflict_sets)
        for solve_args in self.solve_options:
            hs_dag.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(hs_dag.generate_minimal_hitting_sets()))
            self.assertTrue(hs_dag.verify())

    def test_solving_minimal_unsorted_conflict_sets_2(self):
        conflict_sets = [{3, 4, 5}, {1}]
        expected_mhs = [{1, 3}, {1, 4}, {1, 5}]
        hs_dag = HsDag(conflict_sets)
        for solve_args in self.solve_options:
            hs_dag.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(hs_dag.generate_minimal_hitting_sets()))
            self.assertTrue(hs_dag.verify())

    def test_solving_minimal_sorted_conflict_sets_2(self):
        conflict_sets = [{1}, {3, 4, 5}]
        expected_mhs = [{1, 3}, {1, 4}, {1, 5}]
        hs_dag = HsDag(conflict_sets)
        for solve_args in self.solve_options:
            hs_dag.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(hs_dag.generate_minimal_hitting_sets()))
            self.assertTrue(hs_dag.verify())

    def test_solving_nonminimal_sorted_conflict_sets_1(self):
        conflict_sets = [{1, 2}, {3, 4}, {1, 2, 5}]
        expected_mhs = [{1, 3}, {1, 4}, {2, 3}, {2, 4}]
        hs_dag = HsDag(conflict_sets)
        for solve_args in self.solve_options:
            hs_dag.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(hs_dag.generate_minimal_hitting_sets()))
            self.assertTrue(hs_dag.verify())

    def test_solving_nonminimal_unsorted_conflict_sets_1(self):
        conflict_sets = [{1, 2, 5}, {1, 2}, {3, 4}]
        expected_mhs = [{1, 3}, {1, 4}, {2, 3}, {2, 4}]
        hs_dag = HsDag(conflict_sets)
        for solve_args in self.solve_options:
            hs_dag.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(hs_dag.generate_minimal_hitting_sets()))
