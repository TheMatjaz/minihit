#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

from anytree import Node

from . import mhs

class RcTree(mhs.MinimalHittingSetProblem):
    def __init__(self, conflict_sets):
        super().__init__(conflict_sets)
        self.tree = RcTreeNode("root")

    def solve(self):
        self.sort_confict_sets_by_cardinality()


class RcTreeNode(Node):
    def __init__(self, name, label = None, **kwargs):
        super().__init__(name, **kwargs)
        self.label = label
        self.checked = False
        self.theta_set = set()

    def close(self):
        pass


