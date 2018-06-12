#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

from typing import List

from . import hsdag


class RcTreeNode(hsdag.HsDagNode):
    def __init__(self):
        super().__init__()
        self.prohibited_edges = set()  # a.k.a. theta(node)
        self.existing_edges = set()  # a.k.a. theta_c(node)


class RcTree(hsdag.HsDag):
    def __init__(self, set_of_conflicts: List[set] = None):
        super().__init__(set_of_conflicts)

    def _prepare_to_process_nodes(self, sort: bool):
        self._clone_set_of_conflicts(sort)
        self.root = RcTreeNode()
        self.amount_of_nodes_constructed += 1
        self.nodes_to_process.append(self.root)

    def _relabel_and_trim(self, node_in_processing: RcTreeNode,
                          other_node: RcTreeNode):
        difference = node_in_processing.label.difference(other_node.label)
        other_node.label = node_in_processing.label
        for conflict in difference:
            self._trim_subdag(other_node, conflict)
            self._update_prohibited_edges_and_create_allowed_children(
                other_node, difference)
            try:
                self._working_set_of_conflicts.remove(other_node.label)
            except ValueError as label_not_in_conflicts:
                pass

    def _update_prohibited_edges_and_create_allowed_children(
            self, other_node: RcTreeNode, difference: set):
        for descendant in self.breadth_first_explore(other_node):
            descendant.prohibited_edges.symmetric_difference_update(difference)
            self._create_children(descendant)

    def _create_children(self, node_in_processing: RcTreeNode):
        conflicts_generating_edges = \
            node_in_processing.label.difference(
                node_in_processing.prohibited_edges)
        for conflict in conflicts_generating_edges:
            node_in_processing.children[conflict] = None
            child_node = self._child_node(node_in_processing, conflict)
            node_in_processing.children[conflict] = child_node
            self.nodes_to_process.append(child_node)

    def _child_node(self, node_in_processing: RcTreeNode, conflict):
        child_node = RcTreeNode()
        self.amount_of_nodes_constructed += 1
        child_node.existing_edges = node_in_processing.label.intersection(
            node_in_processing.children.keys())
        child_node.prohibited_edges = child_node.existing_edges.union(
            node_in_processing.prohibited_edges)
        child_node.parents[conflict] = node_in_processing
        child_node.path_from_root.update(node_in_processing.path_from_root)
        child_node.path_from_root.add(conflict)
        return child_node
