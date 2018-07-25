#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.
import abc
from typing import Generator


class SolutionSet(set):
    """
    Extension of a Python set that can also verify if it's hitting
    or minimal-hitting against a collection of other sets.
    """

    def is_hitting(self, sets):
        """
        Verifies if this object is a hitting set for the collection of sets.

        A hitting set of a collection of sets has a non-empty intersection
        with each set in the collection.

        Args:
            sets (Iterable[set]): the collection to check against.

        Returns:
            bool: True if hitting, False otherwise.
        """
        if len(self) == 0:
            return False
        for other_set in sets:
            if self.isdisjoint(other_set):
                return False
        return True

    def is_minimal_hitting(self, sets):
        """
        Verifies if this object is a minimal hitting set for the collection
        of sets.

        A hitting set of a collection of sets has a non-empty intersection
        with each set in the collection. A minimal hitting set is a hitting
        set that has no subsets that are still hitting sets for the same
        collection.

        Args:
            sets (Iterable[set]): the collection to check against.

        Returns:
            bool: True if hitting and minimal, False otherwise.
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


class MinimalHittingSetsProblem(abc.ABC):
    """
    Representation of a minimal hitting set problem with a solver algorithm
    and generator of all minimal hitting sets for a list of conflicts.
    """

    def __init__(self, list_of_conflicts=None):
        """
        Constructs the minimal hitting sets problem to be solved with an
        optional list of conflicts to initialize it.

        Args:
            list_of_conflicts (List[set]): conflicts to find the minimal
                hitting sets for.
        """
        self._working_list_of_conflicts = None
        self.list_of_conflicts = list_of_conflicts
        self.amount_of_nodes_constructed = 0

    def _clone_list_of_conflicts(self, sort):
        if sort:
            # noinspection PyTypeChecker
            self._working_list_of_conflicts = sorted(self.list_of_conflicts,
                                                    key=len)
        else:
            if isinstance(self.list_of_conflicts, Generator):
                self.list_of_conflicts = list(self.list_of_conflicts)
            self._working_list_of_conflicts = self.list_of_conflicts.copy()

    @abc.abstractmethod
    def solve(self, **kwargs):
        """
        Runs the algorithm that finds the minimal hitting sets for the
        list of conflicts.

        Args:
            **kwargs: arguments the solving algorithm may take.

        Returns:
            float: elapsed execution time in seconds.
        """
        pass

    @abc.abstractmethod
    def reset(self):
        """
        Erases the state of the solver, forgetting all found solutions.
        """
        pass

    @abc.abstractmethod
    def generate_minimal_hitting_sets(self):
        """
        Provides a generator of the minimal hitting sets computed by the
        solving algorithm.

        Run `solve()` first to obtain any results.

        Returns:
            Generator[SolutionSet, None, None]: generator of the solutions
                (minimal hitting sets) of the list of conflicts.
        """
        pass

    def verify(self):
        """
        Double checks whether the computed minimal hitting sets are really
        minimal hitting sets.

        Used mostly for testing and debugging.

        Returns:
            bool: True if the verification is successful, False otherwise.
        """
        for mhs_candidate in self.generate_minimal_hitting_sets():
            if not mhs_candidate.is_minimal_hitting(self.list_of_conflicts):
                return False
        return True

    @abc.abstractmethod
    def render(self, out_file=None):
        """
        Generates and opens a rendering of the graph used to find the minimal
        hitting sets, if any is available.

        Args:
            out_file (str): name of the file where to save the rendering.
                If None, the file is saved to the system's temporary directory.
        """
        pass
