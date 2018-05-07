#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

from . import mhs


class HsDag(mhs.MinimalHittingSetProblem):
    def __init__(self, conflict_sets):
        super().__init__(conflict_sets)
        self.dag = HsDagNode("root")

    def solve(self):
        self.sort_confict_sets_by_cardinality()


class HsDagNode(object):
    def __init__(self, name, label, **kwargs):
        self.name = name
        self.label = label
        self.checked = False
        self.pointing_to = set()

    def close(self):
        pass

    def add_pointed_to(self, pointed_node):
        if not isinstance(HsDagNode):
            raise ValueError(
                "A pointed-to node should be of class {:s}".format(
                    self.__class__.__name__))
        self.pointing_to.add(pointed_node)
