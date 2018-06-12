#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.
import queue
from typing import List

from . import hsdag


class RcTreeNode(hsdag.HsDagNode):
    def __init__(self):
        super().__init__()
        self.theta = set()  # a.k.a. theta(node)
        self.theta_c = set()  # a.k.a. theta_c(node)


class RcTree(hsdag.HsDag):
    def __init__(self, conflict_sets: List[set] = None):
        super().__init__(conflict_sets)

    def _prepare_to_process_nodes(self, sort_beforehand: bool):
        self._clone_conflict_sets(sort_beforehand)
        self.root = RcTreeNode()
        self.amount_of_nodes_constructed += 1
        self.nodes_to_process.append(self.root)

    def _relabel_and_trim(self, node_in_processing: RcTreeNode,
                          other_node: RcTreeNode):
        difference = node_in_processing.label.difference(other_node.label)
        other_node.label = node_in_processing.label
        for conflict in difference:
            self._trim_subdag(other_node, conflict)
            self._update_thetas_and_create_allowed_children(other_node,
                                                            difference)
            try:
                self._working_conflict_sets.remove(other_node.label)
            except ValueError as label_not_in_conflicts:
                pass

    def _update_thetas_and_create_allowed_children(
            self, other_node: RcTreeNode, difference: set):
        for descendant in self.breadth_first_explore(other_node):
            descendant.theta.difference_update(difference)
            self._create_children(descendant)

    def _create_children(self, node_in_processing: RcTreeNode):
        conflicts_generating_edges = \
            node_in_processing.label.difference(node_in_processing.theta)
        for conflict in conflicts_generating_edges:
            node_in_processing.children[conflict] = None
            child_node = self._child_node(node_in_processing, conflict)
            node_in_processing.children[conflict] = child_node
            self.nodes_to_process.append(child_node)

    def _child_node(self, node_in_processing: RcTreeNode, conflict):
        child_node = RcTreeNode()
        self.amount_of_nodes_constructed += 1
        child_node.theta_c = node_in_processing.label.intersection(
            node_in_processing.children.keys())
        child_node.theta = child_node.theta_c.union(node_in_processing.theta)
        child_node.parents[conflict] = node_in_processing
        child_node.path_from_root.update(node_in_processing.path_from_root)
        child_node.path_from_root.add(conflict)
        return child_node
