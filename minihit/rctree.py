#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2018, Matjaž Guštin <dev@matjaz.it> https://matjaz.it
# All rights reserved.
# This file is part of the MiniHit project which is released under
# the BSD 3-clause license.

from . import hsdag


class RcTreeNode(hsdag.HsDagNode):
    def __init__(self):
        super().__init__()
        self.conflict_set = set()
        self.excluded_set = set()
        self.parent = None
        del self.parents


class RcTree(hsdag.HsDag):
    def __init__(self, conflict_sets):
        super().__init__(conflict_sets)

    def _prepare_to_process_nodes(self, sort_beforehand: bool):
        pass  # TODO

    def _process_nodes(self, prune: bool):
        pass  # TODO
