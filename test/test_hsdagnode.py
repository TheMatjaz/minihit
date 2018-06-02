#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import TestCase

from minihit.hsdag import HsDagNode


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
