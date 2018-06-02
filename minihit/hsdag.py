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


class HsDag(mhs.MinimalHittingsetProblem):
    def __init__(self, conflict_sets: List[set]):
        super().__init__(conflict_sets)
        self.root = None
        self.nodes_to_process = queue.deque()

    def minimal_hitting_sets(self) -> Generator[mhs.SolutionSet, None, None]:
        for node in self.nodes:
            if node.is_ticked:
                yield mhs.SolutionSet(node.path_from_root)

    def solve(self):
        if not self.conflict_sets:
            # Empty list of conflict sets, nothing to do
            return
        self._sort_confict_sets_by_cardinality()
        self.root = HsDagNode()
        self.nodes_to_process.append(self.root)
        while self.nodes_to_process:
            processed_node = self.nodes_to_process.pop()
            # TODO Closing here
            self._label_node(processed_node)
            # TODO Pruning here
            if processed_node.label is not None:
                self._generate_edges(processed_node)

    def _label_node(self, processed_node: HsDagNode):
        for conflict_set in self.conflict_sets:
            if conflict_set.isdisjoint(processed_node.path_from_root):
                processed_node.label = conflict_set
                return
        processed_node.tick()

    def _generate_edges(self, processed_node: HsDagNode):
        for conflict in processed_node.label:
            # TODO Reusing nodes here
            child_node = HsDagNode()
            child_node.parents[conflict] = processed_node
            child_node.path_from_root.append(conflict)
            processed_node.children[conflict] = child_node
            self.nodes_to_process.append(child_node)

    #
    #     for conflict_set in self.conflict_sets:
    #         processed_node = HsDagNode()
    #         self._process_node(processed_node)
    #
    #
    #         try:
    #             unlabeled_node = self.nodes_to_process.pop()
    #             processed_node = HsDagNode()
    #             self._attempt_closing_node(processed_node)
    #             if processed_node.is_closed:
    #                 continue
    #             self._attempt_labeling_node(processed_node)
    #             # TODO: Pruning here
    #             if processed_node.label is not None:
    #                 self._generate_edges(processed_node)
    #             if len(self.nodes) == 0:
    #                 self.root = processed_node
    #             self.nodes.append(processed_node)
    #         except IndexError as no_more_unlabeled_nodes:
    #             return
    #
    #     while self.nodes_to_process:
    #         unlabeled_node = self.nodes_to_process.pop()
    #
    #         for processed_node in []:
    #             if self._attempt_closing_node(processed_node):
    #                 continue
    #             self._attempt_labeling_node(processed_node)
    #             if self.pruning_enabled:
    #                 removed_processed_node = self._pruning(processed_node)
    #                 if removed_processed_node:
    #                     continue
    #             self.used_conflict_sets.add(current
    #             conflict
    #             set)
    #             if processed_node still usable:
    #                 self.nodes.append(processed_node)
    #
    # def _attempt_closing_node(self, processed_node: HsDagNode):
    #     # Step 1 of the algorithm
    #     for other_node in self.nodes:
    #         if (other_node.path_from_root.issubset(
    # processed_node.path_from_root)
    #                 and other_node.is_ticked):
    #             processed_node.close()
    #
    #
    #
    #
    # def _pruning(self, processed_node: HsDagNode):
    #     # Step 3 of the algorithm.
    #     if processed_node.label not in self.used_conflict_sets:
    #         for other_node in self.nodes:
    #             if processed_node.label.issubset(other_node.label):
    #                 # Step 3a of the algorithm.
    #                 removed_processed_node = self._step_a(processed_node,
    # other_node)
    #                 if removed_processed_node:
    #                     return True
    #                 else:
    #                     self._step_b(other_node)
    #     return False
    #
    # def _step_a(self, processed_node: HsDagNode, other_node: HsDagNode):
    #     difference = processed_node.label.difference(other_node.label)
    #     other_node.label = processed_node.label
    #     for conflict in difference:
    #         try:
    #             node_to_remove = other_node.edges_to_children[conflict]
    #             other_node.blocked_edges.add(conflict)
    #             self._remove(node_to_remove)
    #             if node_to_remove is processed_node:
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
    # def _find_new_edge_destination(self, processed_node: HsDagNode,
    # conflict):
    #     for other_node in self.nodes:
    #         if (other_node.path_from_root ==
    # processed_node.path_from_root.union(
    #                 conflict)):
    #             return other_node
    #     new_edge_destination = HsDagNode()
    #     self.nodes_to_process.append(new_edge_destination)
    #     return new_edge_destination
