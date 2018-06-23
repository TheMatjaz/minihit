#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase

from minihit.rctree import RcTree, RcTreeNode


class TestRcTreeNode(TestCase):
    def test_default_constructor(self):
        node = RcTreeNode()
        self.assertFalse(node.is_ticked)
        self.assertFalse(node.is_closed)
        self.assertEqual(0, len(node.path_from_root))
        self.assertEqual(0, len(node.children))
        self.assertIsNone(node.label)

    def test_closing(self):
        node = RcTreeNode()
        self.assertFalse(node.is_closed)
        node.close()
        self.assertTrue(node.is_closed)

    def test_ticking(self):
        node = RcTreeNode()
        self.assertFalse(node.is_ticked)
        node.tick()
        self.assertTrue(node.is_ticked)

    def test_ticking_removes_label(self):
        node = RcTreeNode()
        self.assertFalse(node.is_ticked)
        node.label = {1, 2, 3}
        node.tick()
        self.assertIsNone(node.label)

    def test_cannot_relabel_already_ticked(self):
        node = RcTreeNode()
        node.tick()
        with self.assertRaises(ValueError):
            node.label = {667, 987564}

    def test_can_relabel_non_ticked(self):
        node = RcTreeNode()
        node.label = {1, 2, 3}
        self.assertEqual({1, 2, 3}, node.label)
        node.label = {9}
        self.assertEqual({9}, node.label)


class TestRcTree(TestCase):
    def setUp(self):
        self.solve_options = [
            (False, False),
            (False, True),
            (True, False),
            (True, True),
        ]

    def test_empty_list_of_conflicts_does_nothing(self):
        rc_tree = RcTree([])
        for solve_args in self.solve_options:
            elapsed = rc_tree.solve(*solve_args)
            self.assertEqual(0, len(rc_tree.nodes))
            self.assertEqual([], list(rc_tree.generate_minimal_hitting_sets()))
            self.assertIsNone(rc_tree.root)
            self.assertTrue(elapsed < 0.5)
            self.assertTrue(rc_tree.verify())
            self.assertEqual(len(rc_tree.nodes),
                             len(list(rc_tree.breadth_first_explore(rc_tree.root))))

    def test_solving_minimal_sorted_list_of_conflicts_1(self):
        list_of_conflicts = [{1, 3}, {1, 4}]
        expected_mhs = [{1}, {3, 4}]
        rc_tree = RcTree(list_of_conflicts)
        for solve_args in self.solve_options:
            rc_tree.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(rc_tree.generate_minimal_hitting_sets()))
            self.assertTrue(rc_tree.verify())
            self.assertEqual(len(rc_tree.nodes),
                             len(list(rc_tree.breadth_first_explore(rc_tree.root))))

    def test_solving_minimal_unsorted_list_of_conflicts_2(self):
        list_of_conflicts = [{3, 4, 5}, {1}]
        expected_mhs = [{1, 3}, {1, 4}, {1, 5}]
        rc_tree = RcTree(list_of_conflicts)
        for solve_args in self.solve_options:
            rc_tree.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(rc_tree.generate_minimal_hitting_sets()))
            self.assertTrue(rc_tree.verify())
            self.assertEqual(len(rc_tree.nodes),
                             len(list(rc_tree.breadth_first_explore(rc_tree.root))))

    def test_solving_minimal_sorted_list_of_conflicts_2(self):
        list_of_conflicts = [{1}, {3, 4, 5}]
        expected_mhs = [{1, 3}, {1, 4}, {1, 5}]
        rc_tree = RcTree(list_of_conflicts)
        for solve_args in self.solve_options:
            rc_tree.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(rc_tree.generate_minimal_hitting_sets()))
            self.assertTrue(rc_tree.verify())
            self.assertEqual(len(rc_tree.nodes),
                             len(list(rc_tree.breadth_first_explore(rc_tree.root))))

    def test_solving_nonminimal_sorted_list_of_conflicts_1(self):
        list_of_conflicts = [{1, 2}, {3, 4}, {1, 2, 5}]
        expected_mhs = [{1, 3}, {1, 4}, {2, 3}, {2, 4}]
        rc_tree = RcTree(list_of_conflicts)
        for solve_args in self.solve_options:
            rc_tree.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(rc_tree.generate_minimal_hitting_sets()))
            self.assertTrue(rc_tree.verify())
            self.assertEqual(len(rc_tree.nodes),
                             len(list(rc_tree.breadth_first_explore(rc_tree.root))))

    def test_solving_nonminimal_unsorted_list_of_conflicts_1(self):
        list_of_conflicts = [{1, 2, 5}, {1, 2}, {3, 4}]
        expected_mhs = [{1, 3}, {1, 4}, {2, 3}, {2, 4}]
        rc_tree = RcTree(list_of_conflicts)
        for solve_args in self.solve_options:
            rc_tree.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(rc_tree.generate_minimal_hitting_sets()))
            self.assertTrue(rc_tree.verify())
            self.assertEqual(len(rc_tree.nodes),
                             len(list(rc_tree.breadth_first_explore(rc_tree.root))))

    def test_solving_nonminimal_unsorted_list_of_conflicts_2(self):
        list_of_conflicts = [{1, 2, 3, 4}, {3}, {2, 4}, {15}, {9, 2, 15},
                            {9, 3}, {8, 7}, {8, 9, 1, 7}]
        expected_mhs = [{8, 2, 3, 15}, {2, 3, 7, 15}, {8, 3, 4, 15},
                        {3, 4, 7, 15}]
        rc_tree = RcTree(list_of_conflicts)
        for solve_args in self.solve_options:
            rc_tree.solve(*solve_args)
            self.assertEqual(expected_mhs,
                             list(rc_tree.generate_minimal_hitting_sets()))
            self.assertTrue(rc_tree.verify())
            self.assertEqual(len(rc_tree.nodes),
                             len(list(rc_tree.breadth_first_explore(rc_tree.root))))

    def test_solving_does_not_alter_list_of_conflicts(self):
        list_of_conflicts = [{1, 2, 5}, {3, 4}, {1, 2}]
        original_list_of_conflicts = [{1, 2, 5}, {3, 4}, {1, 2}]
        rc_tree = RcTree(list_of_conflicts)
        for solve_args in self.solve_options:
            rc_tree.solve(*solve_args)
            self.assertEqual(original_list_of_conflicts,
                             rc_tree.list_of_conflicts)

    def test_resetting_deletes_everything(self):
        list_of_conflicts_initial = [{1}, {3, 4, 5}]
        rc_tree = RcTree(list_of_conflicts_initial)
        rc_tree.solve()
        rc_tree.reset()
        self.assertEqual(0, len(list(rc_tree.generate_minimal_hitting_sets())))
        self.assertEqual(0, len(rc_tree.nodes))
        self.assertIsNone(rc_tree.root)
        self.assertEqual(0, len(list(rc_tree.breadth_first_explore(rc_tree.root))))
