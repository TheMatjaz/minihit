#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import minihit


def solve_from_file(input_file_name):
    parser = minihit.fileload.ConflictSetsFileParser()
    parser.parse(input_file_name)
    for line, conflict_sets in parser.sets_by_line.items():
        hsdag = minihit.hsdag.HsDag(conflict_sets)
        elapsed_hsdag = hsdag.solve()
        solution_hsdag = list(hsdag.generate_minimal_hitting_sets())
        rctree = minihit.rctree.RcTree(conflict_sets)
        elapsed_rctree = rctree.solve()
        solution_rctree = list(rctree.generate_minimal_hitting_sets())
        report = "Line: {:d}\n" \
                 "Conflict sets: {:}\n" \
                 "HSDAG solution: {:}\n" \
                 "RC-Tree solution: {:}\n" \
                 "Algorithm produce same result: {:}" \
                 "HSDAG runtime: {:f}\n" \
                 "RC-Tree runtime: {:f}".format(
            line,
            conflict_sets,
            solution_hsdag,
            solution_rctree,
            solution_hsdag == solution_rctree,
            elapsed_hsdag,
            elapsed_rctree,
        )
        print(report)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {:s} input_file_name".format(sys.argv[0]))
    else:
        solve_from_file(sys.argv[1])
