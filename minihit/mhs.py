#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.
from typing import Generator, Iterable, List


class SolutionSet(set):
    """
    Extension of a Python set that can also verify if it's hitting
    or minimal-hitting against a collection of other sets.
    """

    def is_hitting(self, sets: Iterable[set]) -> bool:
        """
        Verifies if this object is a hitting set for the collection of sets.

        A hitting sets of a collection of sets has a non-empty intersection
        with each set in the collection.

        Args:
            sets: the collection to check against.

        Returns:
            True if hitting, False otherwise.
        """
        if len(self) == 0:
            return False
        for other_set in sets:
            if self.isdisjoint(other_set):
                return False
        return True

    def is_minimal_hitting(self, sets: Iterable[set]) -> bool:
        """
        Verifies if this object is a minimal hitting set for the collection
        of sets.

        A hitting sets of a collection of sets has a non-empty intersection
        with each set in the collection. A minimal hitting set is a hitting
        set that has no subsets that are still hitting sets for the same
        collection.

        Args:
            sets: the collection to check against.

        Returns:
            True if hitting, False otherwise.
        """
        if len(self) == 0:
            return False
        used_elements = set()
        for other_set in sets:
            intersection = self.intersection(other_set)
            used_elements.update(intersection)
            if not intersection:
                return False
        return used_elements == self

    def __repr__(self):
        return '{' + ', '.join(map(str, self)) + '}'


class MinimalHittingSetsProblem(object):
    """
    Abstract representation of a minimal hitting set problem, to be
    implemented by an actual algorithm that solves it.
    """

    def __init__(self, list_of_conflicts: List[set] = None):
        """
        Constructs the minimal hitting sets problem to be solved with an
        optional list of conflicts to initialize it.

        Args:
            list_of_conflicts: conflicts to find the minimal hitting sets for.
        """
        self._working_list_of_conflicts = None
        self.list_of_conflicts = list_of_conflicts
        self.nodes = set()
        self.amount_of_nodes_constructed = 0

    def _clone_list_of_conflicts(self, sort: bool) -> None:
        if sort:
            # noinspection PyTypeChecker
            self._working_list_of_conflicts = sorted(self.list_of_conflicts,
                                                    key=len)
        else:
            self._working_list_of_conflicts = list(self.list_of_conflicts)

    def solve(self, **kwargs) -> None:
        raise NotImplementedError("Has to be implemented by subclass.")

    def generate_minimal_hitting_sets(self) \
            -> Generator[SolutionSet, None, None]:
        raise NotImplementedError("Has to be implemented by subclass.")

    def verify(self) -> bool:
        """
        Double checks whether the computed minimal hitting sets are really
        minimal hitting sets.

        Returns:
            True if the verification is successful, False otherwise.
        """
        for mhs_candidate in self.generate_minimal_hitting_sets():
            if not mhs_candidate.is_minimal_hitting(self.list_of_conflicts):
                return False
        return True

    def render(self, out_file=None):
        raise NotImplementedError("Has to be implemented by subclass.")
