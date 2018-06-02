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

    def test_cannot_relabel(self):
        node = HsDagNode()
        node.label = {1, 2, 3}
        with self.assertRaises(ValueError):
            node.label = {667, 987564}


class TestHsDag(TestCase):
    def test_empty_conflict_sets_does_nothing(self):
        hs_dag = HsDag([])
        hs_dag.solve()
        self.assertEqual(0, len(hs_dag.nodes))
        self.assertEqual([], list(hs_dag.minimal_hitting_sets()))
        self.assertIsNone(hs_dag.root)

    def test_solving_conflict_sets_1(self):
        conflict_sets = [{1, 3}, {1, 4}]
        expected_mhs = [{1}, {1, 3}, {3, 4}]
        hs_dag = HsDag(conflict_sets)
        hs_dag.solve()
        self.assertEqual(expected_mhs, list(hs_dag.minimal_hitting_sets()))

    def test_solving_conflict_sets_2(self):
        conflict_sets = [{1, 2}, {3, 4}]
        expected_mhs = [{1, 3}, {1, 4}, {2, 3}, {2, 4}]
        hs_dag = HsDag(conflict_sets)
        hs_dag.solve()
        self.assertEqual(expected_mhs, list(hs_dag.minimal_hitting_sets()))

    def test_solving_conflict_sets_3(self):
        self.fail()
        # TODO
