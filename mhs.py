#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.
from typing import Iterable, List


class MinimalHittingsetProblem(object):
    def __init__(self, conflict_sets_list: List[set]):
        if not conflict_sets_list:
            raise ValueError("Empty list of conflict sets")
        self.conflict_sets = conflict_sets_list
        self.minimal_hitting_sets = []

    def sort_confict_sets_by_cardinality(self):
        self.conflict_sets.sort(key=len)

    def solve(self):
        raise NotImplementedError("Has to be implemented by subclass.")


class SolutionSet(set):
    def is_hitting(self, sets: Iterable[set]) -> bool:
        for other_set in sets:
            if self.isdisjoint(other_set):
                return False
        return True

    def is_minimal(self, sets: Iterable[set]) -> bool:
        for other_set in sets:
            if self > other_set:
                return False
        return True

    def is_minimal_hitting_set(self, sets: Iterable[set]) -> bool:
        return self.is_hitting(sets) and self.is_minimal(sets)
