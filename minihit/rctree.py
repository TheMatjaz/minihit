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
        self.theta_c = set()
        self.theta = set()

    @property
    def parent(self):
        if len(self.parents) > 1:
            raise ValueError("There is more than a parent in the tree node.")
        else:
            for parent in self.parents.values():
                return parent
        return None

    @property
    def parent_edge(self):
        if len(self.parents) > 1:
            raise ValueError("There is more than a parent in the tree node.")
        else:
            for edge in self.parents.keys():
                return edge
        return None

    def name_for_render(self):
        format_string = "L: {:s}\nP: {:s}\nT: {:s}\nTc: {:s}"
        if self.is_ticked:
            label = '✓'
        else:
            label = self.label
        if self.is_closed:
            format_string += ", closed"
        return format_string.format(
            str(label),
            str(self.path_from_root),
            '{}' if len(self.theta) == 0 else str(self.theta),
            '{}' if len(self.theta_c) == 0 else str(self.theta_c),
        )


class RcTree(hsdag.HsDag):
    def __init__(self, list_of_conflicts: List[set] = None):
        super().__init__(list_of_conflicts)

    def _prepare_to_process_nodes(self, sort: bool):
        self._clone_list_of_conflicts(sort)
        self.root = RcTreeNode()
        self.amount_of_nodes_constructed += 1
        self.nodes_to_process.append(self.root)

    def _relabel_and_trim(self, node_in_processing: RcTreeNode,
                          other_node: RcTreeNode):
        difference = other_node.label.difference(node_in_processing.label)
        previous_label = other_node.label
        other_node.label = node_in_processing.label
        for conflict in difference:
            other_node.theta_c.discard(conflict)
            self._trim_subdag(other_node, conflict)
        self._propagate_thetas_changes(other_node, difference)
        self._create_newly_allowed_descendants(other_node)
        try:
            self._working_list_of_conflicts.remove(previous_label)
        except ValueError as label_not_in_conflicts:
            pass

    def _propagate_thetas_changes(
            self, other_node: RcTreeNode, difference: set):
        for descendant in self.breadth_first_explore(other_node):
            if descendant is other_node:
                continue  # Children only, skip the subdag root
            descendant.theta_c.difference_update(difference)
            descendant.theta = descendant.theta_c.union(
                descendant.parent.theta)

    def _create_newly_allowed_descendants(self, other_node: RcTreeNode):
        # Children only, not the subdag root
        descendants = queue.deque(other_node.children.values())
        while descendants:
            descendant = descendants.popleft()
            self._create_children(descendant)
            descendants.extend(descendant.children.values())

    @staticmethod
    def _create_all_allowed_edges(node: RcTreeNode):
        if node.label is not None:
            for allowed_edge in node.label.difference(node.theta_c):
                node.children.setdefault(allowed_edge)

    def _create_children(self, node_in_processing: RcTreeNode):
        if node_in_processing.label is None:
            return
        conflicts_generating_edges = \
            node_in_processing.label.difference(
                node_in_processing.theta)
        for conflict in conflicts_generating_edges:
            node_in_processing.children[conflict] = None
            child_node = self._child_node(node_in_processing, conflict)
            node_in_processing.children[conflict] = child_node
            self.nodes_to_process.append(child_node)

    def _child_node(self, node_in_processing: RcTreeNode, conflict):
        child_node = RcTreeNode()
        self.amount_of_nodes_constructed += 1
        child_node.parents[conflict] = node_in_processing
        child_node.path_from_root.update(node_in_processing.path_from_root)
        child_node.path_from_root.add(conflict)
        child_node.theta_c = \
            node_in_processing.label.intersection(
                child_node.parent.children.keys())
        child_node.theta = child_node.theta_c.union(child_node.parent.theta)
        return child_node
