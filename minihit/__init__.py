#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .getconflicts import ConflictSetsFileParser, random_conflicts, linear_conflicts
from .mhs import SolutionSet, MinimalHittingSetsProblem
from .hsdag import HsDag
from .rctree import RcTree
from .algcompare import compare_from_file, compare

VERSION = 'v1.0.1'
