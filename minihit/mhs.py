#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.
from typing import Generator, Iterable, List


class SolutionSet(set):
    def is_hitting(self, sets: Iterable[set]) -> bool:
        if len(self) == 0:
            return False
        for other_set in sets:
            if self.isdisjoint(other_set):
                return False
        return True

    def is_minimal_hitting(self, sets: Iterable[set]) -> bool:
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


class MinimalHittingsetProblem(object):
    def __init__(self, conflict_sets: List[set] = None):
        self._working_conflict_sets = None
        self.conflict_sets = conflict_sets
        self.nodes = []
        self.amount_of_nodes_constructed = 0

    def _clone_conflict_sets(self, sort: bool) -> None:
        if sort:
            self._working_conflict_sets = sorted(self.conflict_sets, key=len)
        else:
            self._working_conflict_sets = self.conflict_sets.copy()

    def solve(self, conflict_sets: List[set], **kwargs) -> None:
        raise NotImplementedError("Has to be implemented by subclass.")

    def generate_minimal_hitting_sets(self) -> Generator[
        SolutionSet, None, None]:
        raise NotImplementedError("Has to be implemented by subclass.")

    def verify(self) -> bool:
        for mhs_candidate in self.generate_minimal_hitting_sets():
            if not mhs_candidate.is_minimal_hitting(self.conflict_sets):
                return False
        return True

    def render(self, out_file=None):
        raise NotImplementedError("Has to be implemented by subclass.")

