#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.
import queue
from typing import List

from . import mhs


class HsDagNode(object):
    _label: set

    def __init__(self, conflict_set):
        self.conflict_set = conflict_set
        self.nodes_from_root = set()  # Aka labels aka h(node)
        self._closed = False
        self._ticked = False
        self._label = None
        self.edges = {}
        self.blocked_edges = set()

    @property
    def is_closed(self):
        return self._closed

    def close(self):
        self._closed = True

    @property
    def is_ticked(self):
        return self._ticked

    def tick(self):
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

        # self.label = label
        # self.conflict_set = conflict_set
        # self.pointing_to = set()
        # self.checked = False
        # self.closed = False
        # self.edge_labels = set()

    def generate_pointed_to(self, next_conflict_set):
        for this_node_conflict in self.conflict_set:
            new_label = self.label \
                .union(set(this_node_conflict))
            new_node = HsDagNode(next_conflict_set, new_label)
            self.pointing_to.add(new_node)


class HsDag(mhs.MinimalHittingsetProblem):
    def __init__(self, conflict_sets: List[set]):
        super().__init__(conflict_sets)
        self.root = HsDagNode(conflict_sets[0])
        self.nodes = [self.root]
        self.used_conflict_sets = set()
        self.unlabeled_nodes = queue.deque()

    def solve(self):
        self.sort_confict_sets_by_cardinality()
        while self.unlabeled_nodes:
            unlabeled_node = self.unlabeled_nodes.pop()

            for new_node in []:
                if self._is_node_skippable(new_node):
                    continue
                self._labeling(new_node)
                removed_new_node = self._pruning(new_node)
                if removed_new_node:
                    continue
                self.used_conflict_sets.add(current
                conflict
                set)
                if new_node still usable:
                    self.nodes.append(new_node)

    def _is_node_skippable(self, new_node: HsDagNode) -> bool:
        # Step 1 of the algorithm a.k.a. Closing
        for other_node in self.nodes:
            if (other_node.nodes_from_root.issubset(new_node.nodes_from_root)
                    and other_node.is_ticked):
                new_node.close()
                return True
        return False

    def _labeling(self, new_node: HsDagNode):
        # Step 2 of the algorithm
        for conflict_set in self.conflict_sets:
            if conflict_set.isdisjoint(new_node.nodes_from_root):
                new_node.label = conflict_set
        new_node.tick()

    def _pruning(self, new_node: HsDagNode):
        # Step 3 of the algorithm.
        if new_node.label not in self.used_conflict_sets:
            for other_node in self.nodes:
                if new_node.label.issubset(other_node.label):
                    # Step 3a of the algorithm.
                    removed_new_node = self._step_a(new_node, other_node)
                    if removed_new_node:
                        return True
                    else:
                        self._step_b(other_node)
        return False

    def _step_a(self, new_node: HsDagNode, other_node: HsDagNode):
        difference = new_node.label.difference(other_node.label)
        other_node.label = new_node.label
        for conflict in difference:
            try:
                node_to_remove = other_node.edges[conflict]
                other_node.blocked_edges.add(conflict)
                self._remove(node_to_remove)
                if node_to_remove is new_node:
                    return True
            except KeyError:
                # No node found with that conflict as edge label
                pass
        return False

    def _remove(self, node_to_remove: HsDagNode):
        # Remove this node and all of its descendants
        # except for those nodes with another ancestor that is not being
        # removed
        pass  # TODO

    def _step_b(self, other_node):
        try:
            self.conflict_sets.remove(other_node.label)
        except KeyError:
            pass

    def _step_4(self, new_node: HsDagNode):
        # if new_node.label is not None: # Probably not needed? Will always
        # be labeled?
        for conflict in new_node.label:
            node_at_end_of_edge = None
            for other_node in self.nodes:
                if other_node.nodes_from_root == \
                        new_node.nodes_from_root.union(
                        conflict):
                    node_at_end_of_edge = other_node
                    break
            if node_at_end_of_edge is None:
                node_at_end_of_edge = HsDagNode()
                self.unlabeled_nodes.append(node_at_end_of_edge)
            new_node.edges[conflict] = node_at_end_of_edge
