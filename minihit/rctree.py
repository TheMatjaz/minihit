#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.
import queue

from . import hsdag


class RcTreeNode(hsdag.HsDagNode):
    def __init__(self):
        super().__init__()
        self.theta = set()  # a.k.a. theta(node)
        self.theta_c = set()  # a.k.a. theta_c(node)
        self.parent = None
        del self.parents

    @property
    def is_orphan(self):
        return bool(self.parent)


class RcTree(hsdag.HsDag):
    def __init__(self, conflict_sets):
        super().__init__(conflict_sets)

    def _prepare_to_process_nodes(self, sort_beforehand: bool):
        if sort_beforehand:
            self._sort_confict_sets_by_cardinality()
        root = RcTreeNode()
        self.nodes_to_process.append(root)

    def _relabel_and_trim(self, node_in_processing: RcTreeNode,
                          other_node: RcTreeNode):
        difference = node_in_processing.label.difference(other_node.label)
        other_node.label = node_in_processing.label
        for conflict in difference:
            self._trim_subdag(other_node, conflict)
            self._update_thetas_and_create_allowed_children(other_node,
                                                            difference)
            self.conflict_sets.remove(other_node.label)

    def _trim_subdag(self, parent_node: RcTreeNode, edge_to_trim):
        try:
            subtree_root_to_remove = parent_node.children.pop(edge_to_trim)
            for descendant in self._descendants(subtree_root_to_remove):
                descendant.children = {}
                descendant.parent = None
                self.nodes.remove(descendant)
            self.nodes.remove(subtree_root_to_remove)
        except KeyError as no_child_with_that_edge:
            pass

    def _update_thetas_and_create_allowed_children(
            self, other_node: RcTreeNode, difference: set):
        for descendant in self._descendants(other_node):
            descendant.theta.difference_update(difference)
            self._create_children(descendant)

    @staticmethod
    def _descendants(root: RcTreeNode):
        # Breadth first search
        descendants = queue.deque(root.children.values())
        while descendants:
            descendant = descendants.popleft()
            descendants.extend(descendant.children.values())
            yield descendant

    def _create_children(self, node_in_processing: RcTreeNode):
        conflicts_generating_edges = node_in_processing.label.difference(
            node_in_processing.theta)
        for conflict in conflicts_generating_edges:
            node_in_processing.children[conflict] = None
            child_node = self._child_node(node_in_processing, conflict)
            node_in_processing.children[conflict] = child_node
            self.nodes_to_process.append(child_node)

    def _child_node(self, node_in_processing: RcTreeNode, conflict):
        child_node = RcTreeNode()
        child_node.theta_c = node_in_processing.label.intersection(
            node_in_processing.children.keys())
        child_node.theta = child_node.theta_c.union(node_in_processing.theta)
        child_node.parent = node_in_processing
        child_node.path_from_root.update(node_in_processing.path_from_root)
        child_node.path_from_root.add(conflict)
        return child_node
