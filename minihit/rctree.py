#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

from collections import deque

from anytree import AnyNode, ContStyle, RenderTree

from . import mhs


class RcTree(mhs.MinimalHittingsetProblem):
    def __init__(self, conflict_sets):
        super().__init__(conflict_sets)
        self.root = RcTreeNode(conflict_sets[0])

    def solve(self):
        self.sort_confict_sets_by_cardinality()
        nodes_to_process = deque([self.root])
        for conflict_set in self.conflict_sets:
            while nodes_to_process:
                node_to_process = nodes_to_process.popleft()
                children = node_to_process.generate_children(conflict_set)
                nodes_to_process.extend(children)

    def __str__(self):
        strings = []
        for pre, _, node in RenderTree(self.root, style=ContStyle()):
            strings.append("{:s}{:s}".format(pre, node.name))
        return '\n'.join(strings)


class RcTreeNode(AnyNode):
    def __init__(self, conflict_set, label=set(), excluded_set=set(),
                 parent=None):
        super().__init__(parent=parent)
        self.label = label
        self.name = str(label)
        self.conflict_set = conflict_set
        self.excluded_set = excluded_set
        self.checked = False
        self.closed = False

    def generate_children(self, next_conflict_set):
        children = []
        excluded_so_far = set()
        for this_node_conflict in self.conflict_set:
            child_label = self.label.union({this_node_conflict})
            child_excluded_set = excluded_so_far.union(self.excluded_set)
            child = RcTreeNode(next_conflict_set,
                               child_label,
                               child_excluded_set,
                               parent=self)
            children.append(child)
            excluded_so_far.add(this_node_conflict)
        return children
