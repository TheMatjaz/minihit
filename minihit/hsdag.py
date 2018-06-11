#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

import queue
import time
from typing import Generator, List

from . import mhs


class HsDagNode(object):
    def __init__(self):
        self.path_from_root = mhs.SolutionSet()  # a.k.a. h(node)
        self.children = dict()
        self.parents = dict()
        self._closed = False
        self._ticked = False
        self._label = None
        self.label = None

    @property
    def is_closed(self):
        return self._closed

    def close(self):
        self._closed = True

    @property
    def is_ticked(self):
        return self._ticked

    def tick(self):
        self._label = None
        self._ticked = True

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, new_label):
        if self._ticked:
            raise ValueError("Node already ticked. Cannot relabel.")
        else:
            self._label = new_label

    @property
    def is_orphan(self):
        return bool(self.parents)

    @property
    def is_childless(self):
        return bool(self.children)

    @property
    def is_not_in_dag(self):
        return self.is_orphan and self.is_childless

    def __str__(self):
        format_string = "HsDagNode, path={:}, label={:}"
        if self.is_ticked:
            label = '✓'
        else:
            label = self.label
        if self.is_closed:
            format_string += ", closed"
        return format_string.format(self.path_from_root, label)


class HsDag(mhs.MinimalHittingsetProblem):
    def __init__(self, conflict_sets: List[set]):
        super().__init__(conflict_sets)
        self.nodes_to_process = queue.deque()
        # Optimization: keep set of paths form root and set of used labels

    @property
    def root(self):
        try:
            return self.nodes[0]
        except IndexError:
            return None

    def generate_minimal_hitting_sets(self) -> Generator[mhs.SolutionSet, None, None]:
        for node in self.nodes:
            if node.is_ticked:
                yield node.path_from_root

    def solve(self, prune: bool = True,
              sort_beforehand: bool = False) -> float:
        start_time = time.time()
        self.reset()
        if self.conflict_sets:
            self._prepare_to_process_nodes(sort_beforehand)
            self._process_nodes(prune)
        return time.time() - start_time

    def reset(self):
        self.amount_of_nodes_constructed = 0
        self.nodes_to_process.clear()
        self.nodes = []

    def _prepare_to_process_nodes(self, sort_beforehand: bool):
        if sort_beforehand:
            self._sort_confict_sets_by_cardinality()
        root = HsDagNode()
        self.amount_of_nodes_constructed += 1
        self.nodes_to_process.append(root)

    def _process_nodes(self, prune: bool):
        while self.nodes_to_process:
            node_in_processing = self.nodes_to_process.popleft()
            self._attempt_closing_node(node_in_processing)
            if node_in_processing.is_closed:
                continue
            self._label_node(node_in_processing)
            if prune:
                self._prune(node_in_processing)
                if node_in_processing.is_not_in_dag:
                    continue
            if node_in_processing.label is not None:
                self._create_children(node_in_processing)
            self.nodes.append(node_in_processing)

    def _attempt_closing_node(self, node_in_processing: HsDagNode):
        for other_node in self.nodes:
            if (other_node.path_from_root.issubset(
                    node_in_processing.path_from_root)
                    and other_node.is_ticked):
                node_in_processing.close()

    def _label_node(self, node_in_processing: HsDagNode):
        for conflict_set in self.conflict_sets:
            if conflict_set.isdisjoint(node_in_processing.path_from_root):
                node_in_processing.label = conflict_set
                return
        node_in_processing.tick()

    def _prune(self, node_in_processing: HsDagNode):
        if not self._label_was_previously_used(node_in_processing):
            for other_node in self.nodes:
                if (not other_node.is_ticked
                        and node_in_processing.label.issubset(
                            other_node.label)):
                    self._relabel_and_trim(node_in_processing, other_node)

    def _label_was_previously_used(self, node_in_processing: HsDagNode):
        if node_in_processing.is_ticked:
            return True
        for node in self.nodes:
            if node_in_processing.label == node.label:
                return True
        return False

    def _relabel_and_trim(self, node_in_processing: HsDagNode,
                          other_node: HsDagNode):
        difference = node_in_processing.label.difference(other_node.label)
        other_node.label = node_in_processing.label
        for conflict in difference:
            self._trim_subdag(other_node, conflict)
            self.conflict_sets.remove(other_node.label)

    def _trim_subdag(self, parent_node: HsDagNode, edge_to_trim):
        parent_to_trim = parent_node
        while parent_to_trim is not None:
            parent_to_trim = self._unlink_child(parent_to_trim, edge_to_trim)

    def _unlink_child(self, parent_node: HsDagNode, edge_to_trim):
        try:
            child_to_remove = parent_node.children.pop(edge_to_trim)
            child_to_remove.parents.pop(edge_to_trim)
            if child_to_remove.is_orphan:
                self.nodes.remove(child_to_remove)
                return child_to_remove
        except KeyError as no_child_with_that_edge:
            return None

    def _create_children(self, node_in_processing: HsDagNode):
        for conflict in node_in_processing.label:
            child_node = self._edge_termination(node_in_processing, conflict)
            child_node.parents[conflict] = node_in_processing
            child_node.path_from_root.update(node_in_processing.path_from_root)
            child_node.path_from_root.add(conflict)
            node_in_processing.children[conflict] = child_node
            self.nodes_to_process.append(child_node)

    def _edge_termination(self, node_in_processing: HsDagNode, conflict
                          ) -> HsDagNode:
        path_with_conflict = node_in_processing.path_from_root.union(
            [conflict])
        self.amount_of_nodes_constructed += 1
        for other_node in self.nodes:
            if other_node.path_from_root == path_with_conflict:
                return other_node
        return HsDagNode()
