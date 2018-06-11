#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from . import hsdag, rctree, fileload


def solve_from_file(input_file_name, render: bool = False,
                    output_files_prefix: str = None):
    parser = fileload.ConflictSetsFileParser()
    parser.parse(input_file_name)
    for line, conflict_sets in parser.sets_by_line.items():
        print("Line: {:d}".format(line))
        solve(conflict_sets, render, output_files_prefix)


def solve(conflict_sets: List[set], render: bool = False,
          output_files_prefix: str = None):
    hs_dag = hsdag.HsDag(conflict_sets)
    elapsed_hsdag = hs_dag.solve()
    solution_hsdag = list(hs_dag.generate_minimal_hitting_sets())
    rc_tree = rctree.RcTree(conflict_sets)
    elapsed_rctree = rc_tree.solve()
    solution_rctree = list(rc_tree.generate_minimal_hitting_sets())
    report = "Conflict sets: {:}\n" \
             "HSDAG solution: {:}\n" \
             "RC-Tree solution: {:}\n" \
             "Algorithm produce same result: {:}\n" \
             "HSDAG runtime [s]: {:f}\n" \
             "RC-Tree runtime [s]: {:f}\n" \
             "RC-Tree faster by: {:f}\n" \
             "HSDAG nodes built: {:d}\n" \
             "RC-Tree nodes built: {:d}\n" \
             "RC-Tree smaller by: {:f}".format(
        conflict_sets,
        solution_hsdag,
        solution_rctree,
        solution_hsdag == solution_rctree,
        elapsed_hsdag,
        elapsed_rctree,
        elapsed_hsdag / elapsed_rctree,
        hs_dag.amount_of_nodes_constructed,
        rc_tree.amount_of_nodes_constructed,
        hs_dag.amount_of_nodes_constructed /
        rc_tree.amount_of_nodes_constructed,
    )
    print(report)
    if render:
        if output_files_prefix:
            hs_dag.render(output_files_prefix + '_hsdag.gv')
            rc_tree.render(output_files_prefix + '_rctree.gv')
        else:
            hs_dag.render()
            rc_tree.render()
