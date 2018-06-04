#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

import queue
from typing import Generator, List

from . import mhs


class HsDagNode(object):
    def __init__(self):
        self.path_from_root = []  # Aka h(node)
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
        if self._ticked or self._label is not None:
            raise ValueError("Node already labeled or ticked. Cannot relabel.")
        else:
            self._label = new_label

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
    nodes_to_process: queue.deque[HsDagNode]

    def __init__(self, conflict_sets: List[set]):
        super().__init__(conflict_sets)
        self.nodes_to_process = queue.deque()

    @property
    def root(self):
        try:
            return self.nodes[0]
        except IndexError:
            return None

    def minimal_hitting_sets(self) -> Generator[mhs.SolutionSet, None, None]:
        for node in self.nodes:
            if node.is_ticked:
                yield mhs.SolutionSet(node.path_from_root)

    def solve(self, with_pruning: bool = True, with_sorting: bool = False):
        if not self.conflict_sets:
            # Empty list of conflict sets, nothing to do
            return
        if with_sorting:
            self._sort_confict_sets_by_cardinality()
        root = HsDagNode()
        self.nodes_to_process.append(root)
        while self.nodes_to_process:
            node_in_processing = self.nodes_to_process.popleft()
            self._attempt_closing_node(node_in_processing)
            if node_in_processing.is_closed:
                continue
            self._label_node(node_in_processing)
            if with_pruning:
                pass
                # TODO Pruning here
            if node_in_processing.label is not None:
                self._generate_edges(node_in_processing)
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

    def _generate_edges(self, node_in_processing: HsDagNode):
        for conflict in node_in_processing.label:
            child_node = self._child_node_potentially_reused(
                node_in_processing,
                conflict)
            child_node.parents[conflict] = node_in_processing
            child_node.path_from_root.extend(node_in_processing.path_from_root)
            child_node.path_from_root.append(conflict)
            node_in_processing.children[conflict] = child_node
            self.nodes_to_process.append(child_node)

    def _child_node_potentially_reused(self, node_in_processing: HsDagNode,
                                       conflict) -> HsDagNode:
        node_in_processing_path_with_conflict = \
            set(node_in_processing.path_from_root).union(conflict)
        for other_node in self.nodes:
            if other_node.path_from_root == \
                    node_in_processing_path_with_conflict:
                return other_node
        return HsDagNode()

    #
    #     for conflict_set in self.conflict_sets:
    #         node_in_processing = HsDagNode()
    #         self._process_node(node_in_processing)
    #
    #
    #         try:
    #             unlabeled_node = self.nodes_to_process.pop()
    #             node_in_processing = HsDagNode()
    #             self._attempt_closing_node(node_in_processing)
    #             if node_in_processing.is_closed:
    #                 continue
    #             self._attempt_labeling_node(node_in_processing)
    #             # TODO: Pruning here
    #             if node_in_processing.label is not None:
    #                 self._generate_edges(node_in_processing)
    #             if len(self.nodes) == 0:
    #                 self.root = node_in_processing
    #             self.nodes.append(node_in_processing)
    #         except IndexError as no_more_unlabeled_nodes:
    #             return
    #
    #     while self.nodes_to_process:
    #         unlabeled_node = self.nodes_to_process.pop()
    #
    #         for node_in_processing in []:
    #             if self._attempt_closing_node(node_in_processing):
    #                 continue
    #             self._attempt_labeling_node(node_in_processing)
    #             if self.pruning_enabled:
    #                 removed_node_in_processing = self._pruning(
    # node_in_processing)
    #                 if removed_node_in_processing:
    #                     continue
    #             self.used_conflict_sets.add(current
    #             conflict
    #             set)
    #             if node_in_processing still usable:
    #                 self.nodes.append(node_in_processing)
    #
    # def _attempt_closing_node(self, node_in_processing: HsDagNode):
    #     # Step 1 of the algorithm
    #     for other_node in self.nodes:
    #         if (other_node.path_from_root.issubset(
    # node_in_processing.path_from_root)
    #                 and other_node.is_ticked):
    #             node_in_processing.close()
    #
    #
    #
    #
    # def _pruning(self, node_in_processing: HsDagNode):
    #     # Step 3 of the algorithm.
    #     if node_in_processing.label not in self.used_conflict_sets:
    #         for other_node in self.nodes:
    #             if node_in_processing.label.issubset(other_node.label):
    #                 # Step 3a of the algorithm.
    #                 removed_node_in_processing = self._step_a(
    # node_in_processing,
    # other_node)
    #                 if removed_node_in_processing:
    #                     return True
    #                 else:
    #                     self._step_b(other_node)
    #     return False
    #
    # def _step_a(self, node_in_processing: HsDagNode, other_node: HsDagNode):
    #     difference = node_in_processing.label.difference(other_node.label)
    #     other_node.label = node_in_processing.label
    #     for conflict in difference:
    #         try:
    #             node_to_remove = other_node.edges_to_children[conflict]
    #             other_node.blocked_edges.add(conflict)
    #             self._remove(node_to_remove)
    #             if node_to_remove is node_in_processing:
    #                 return True
    #         except KeyError:
    #             # No node found with that conflict as edge label
    #             pass
    #     return False
    #
    # def _remove(self, node_to_remove: HsDagNode):
    #     # Remove this node and all of its descendants
    #     # except for those nodes with another ancestor that is not being
    #     # removed
    #     pass  # TODO
    #
    # def _step_b(self, other_node):
    #     try:
    #         self.conflict_sets.remove(other_node.label)
    #     except KeyError:
    #         pass
    #
    # def _find_new_edge_destination(self, node_in_processing: HsDagNode,
    # conflict):
    #     for other_node in self.nodes:
    #         if (other_node.path_from_root ==
    # node_in_processing.path_from_root.union(
    #                 conflict)):
    #             return other_node
    #     new_edge_destination = HsDagNode()
    #     self.nodes_to_process.append(new_edge_destination)
    #     return new_edge_destination
