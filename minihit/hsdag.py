#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

import queue
import time
from typing import Generator

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
        return len(self.parents) == 0

    @property
    def is_childless(self):
        return len(self.children) == 0

    @property
    def is_not_in_dag(self):
        return self.is_orphan and self.is_childless

    def __str__(self):
        format_string = "(Label: {:s}, Path: {:s})"
        if self.is_ticked:
            label = '✓'
        else:
            label = self.label
        if self.is_closed:
            format_string += ", closed"
        return format_string.format(str(label), str(self.path_from_root))

    def __repr__(self):
        return self.__str__()

    def name_for_render(self):
        format_string = "L: {:s}\nP: {:s}"
        if self.is_ticked:
            label = '✓'
        else:
            label = self.label
        if self.is_closed:
            format_string += ", closed"
        return format_string.format(str(label), str(self.path_from_root))


class HsDag(mhs.MinimalHittingSetsProblem):
    def __init__(self, list_of_conflicts=None):
        super().__init__(list_of_conflicts)
        self.nodes_to_process = queue.deque()
        self.root = None

    def generate_minimal_hitting_sets(self):
        for node in self.breadth_first_explore(self.root):
            if node.is_ticked:
                yield node.path_from_root

    def render(self, out_file=None):
        from graphviz import Digraph
        graph = Digraph(comment=self.__class__.__name__)
        for node in self.breadth_first_explore(self.root):
            node_id = str(node.path_from_root)
            graph.node(node_id, node.name_for_render())
            for conflict, child in node.children.items():
                child_name = str(child.path_from_root)
                graph.edge(node_id,
                           child_name,
                           label=str(conflict))
        if out_file is None:
            out_file = self._get_temp_file_name()
        graph.render(out_file, view=True)

    def _get_temp_file_name(self):
        import tempfile
        import os
        out_file = os.path.join(
            tempfile.gettempdir(),
            'temp_{:s}'.format(self.__class__.__name__))
        return out_file

    def solve(self, prune=True, sort=False):
        """
        Runs the algorithm that finds the minimal hitting sets for the
        list of conflicts.

        Args:
            prune (bool): activates the pruning of the DAG during its
                construction. This reduces data redundancy.
            sort (bool): sorts the list of conflicts by cardinality of the
                conflicts before executing the solving algorithm. This
                completely removes the need for pruning (thus also deactivates
                it automatically). A sorted list of conflicts is the
                best-case scenario for the algorithm.

        Returns:
            float: elapsed execution time in seconds.
        """
        start_time = time.time()
        self.reset()
        if self.list_of_conflicts:
            self._prepare_to_process_nodes(sort)
            if sort:
                prune = False
            self._process_nodes(prune)
            self._working_list_of_conflicts = None  # To reduce used memory
        return time.time() - start_time

    def reset(self):
        self.amount_of_nodes_constructed = 0
        self.nodes_to_process.clear()
        self.root = None
        self._working_list_of_conflicts = None

    def _prepare_to_process_nodes(self, sort: bool):
        self._clone_list_of_conflicts(sort)
        self.root = HsDagNode()
        self.amount_of_nodes_constructed += 1
        self.nodes_to_process.append(self.root)

    def _process_nodes(self, prune: bool):
        while self.nodes_to_process:
            node_in_processing = self.nodes_to_process.popleft()
            self._attempt_closing_node(node_in_processing)
            if node_in_processing.is_closed:
                self._remove_closed_node(node_in_processing)
                continue
            self._label_node(node_in_processing)
            if not self.root.is_childless and prune:
                self._prune(node_in_processing)
                if node_in_processing.is_not_in_dag:
                    continue
            if node_in_processing.label is not None:
                self._create_children(node_in_processing)

    def _attempt_closing_node(self, node_in_processing: HsDagNode):
        for other_node in self.breadth_first_explore(self.root):
            if (other_node.path_from_root < node_in_processing.path_from_root
                    and other_node.is_ticked):
                node_in_processing.close()
                return

    @staticmethod
    def _remove_closed_node(node: HsDagNode):
        for conflict, parent in node.parents.items():
            parent.children.pop(conflict)
        node.parents.clear()

    def _label_node(self, node_in_processing: HsDagNode):
        for conflict_set in self._working_list_of_conflicts:
            if conflict_set.isdisjoint(node_in_processing.path_from_root):
                node_in_processing.label = conflict_set
                return
        node_in_processing.tick()

    def _prune(self, node_in_processing: HsDagNode):
        if not self._label_was_previously_used(node_in_processing):
            for other_node in list(self.breadth_first_explore(self.root)):
                if (other_node.label is not None
                        and node_in_processing.label < other_node.label):
                    self._relabel_and_trim(node_in_processing, other_node)

    def _label_was_previously_used(self, node_in_processing: HsDagNode):
        if node_in_processing.label is None:
            return True
        for node in self.breadth_first_explore(self.root):
            if (node_in_processing is not node
                    and node_in_processing.label == node.label):
                return True
        return False

    def _relabel_and_trim(self, node_in_processing: HsDagNode,
                          other_node: HsDagNode):
        difference = other_node.label.difference(node_in_processing.label)
        previous_label = other_node.label
        other_node.label = node_in_processing.label
        for conflict in difference:
            self._trim_subdag(other_node, conflict)
            try:
                self._working_list_of_conflicts.remove(previous_label)
            except ValueError as label_not_in_conflicts:
                pass

    def _trim_subdag(self, parent_node: HsDagNode, edge_to_trim):
        try:
            subdag_root_to_remove = parent_node.children.pop(edge_to_trim)
            subdag_root_to_remove.parents.pop(edge_to_trim)
        except KeyError:
            return
        for subdag_node in list(
                self.breadth_first_explore(subdag_root_to_remove)):
            self._unlink_immediate_children_from_parent(subdag_node)
            if subdag_node.is_orphan:
                del subdag_node

    @staticmethod
    def _unlink_immediate_children_from_parent(generation_parent):
        for edge, child in generation_parent.children.items():
            child.parents.pop(edge)
        generation_parent.children = {}

    @staticmethod
    def breadth_first_explore(root):
        """Generator of the nodes in the subdag starting from the passed node,
        including it, in breadth-first order.

        Modifications of the subdag between yields of this generator
        may be done by the user of the generator.

        Args:
            root (HsDagNode): first node to be returned and starting
                point of the subdag search.

        Returns:
            Generator[HsDagNode, None, None]: nodes in the subdag in
                breadth-first order.
        """
        if not root:
            return
        visited = set()
        descendants = queue.deque()
        descendants.append(root)
        visited.add(root)
        while descendants:
            descendant = descendants.popleft()
            for child in descendant.children.values():
                if child not in visited:
                    descendants.append(child)
                    visited.add(child)
            yield descendant

    def _create_children(self, node_in_processing: HsDagNode):
        for conflict in node_in_processing.label:
            child_node = self._edge_termination(node_in_processing, conflict)
            child_node.parents[conflict] = node_in_processing
            child_node.path_from_root.update(node_in_processing.path_from_root)
            child_node.path_from_root.add(conflict)
            node_in_processing.children[conflict] = child_node

    def _edge_termination(self, node_in_processing: HsDagNode, conflict
                          ) -> HsDagNode:
        path_with_conflict = node_in_processing.path_from_root.union(
            [conflict])
        for other_node in self.breadth_first_explore(self.root):
            if other_node.path_from_root == path_with_conflict:
                return other_node
        self.amount_of_nodes_constructed += 1
        new_node = HsDagNode()
        self.nodes_to_process.append(new_node)
        return new_node
