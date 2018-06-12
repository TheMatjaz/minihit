#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from . import hsdag, rctree, fileload


def solve_from_file(input_file_name, render: bool = False,
                    output_files_prefix: str = None, prune: bool = True,
                    sort: bool = False):
    parser = fileload.ConflictSetsFileParser()
    parser.parse(input_file_name)
    for line, conflict_sets in parser.sets_by_line.items():
        print("Line: {:d}".format(line))
        solve(conflict_sets, render, output_files_prefix, prune, sort)


def solve(conflict_sets: List[set], render: bool = False,
          output_files_prefix: str = None, prune: bool = True,
          sort: bool = False):
    hs_dag = hsdag.HsDag(conflict_sets)
    elapsed_hsdag = hs_dag.solve(prune=prune, sort_beforehand=sort)
    solution_hsdag = list(hs_dag.generate_minimal_hitting_sets())
    rc_tree = rctree.RcTree(conflict_sets)
    elapsed_rctree = rc_tree.solve(prune=prune, sort_beforehand=sort)
    solution_rctree = list(rc_tree.generate_minimal_hitting_sets())
    report = "Conflict sets: {:}\n" \
             "HSDAG solution: {:}\n" \
             "RC-Tree solution: {:}\n" \
             "Algorithm produce same result: {:}\n" \
             "HSDAG runtime [s]: {:f}\n" \
             "RC-Tree runtime [s]: {:f}\n" \
             "HSDAG/RC-Tree runtime [%]: {:7.3f}\n" \
             "HSDAG nodes constructed: {:d}\n" \
             "RC-Tree nodes constructed: {:d}\n" \
             "RC-Tree/HSDAG constructions [%]: {:7.3f}\n" \
             "HSDAG nodes: {:d}\n" \
             "RC-Tree nodes: {:d}\n" \
             "RC-Tree/HSDAG nodes [%]: {:7.3f}".format(
        conflict_sets,
        solution_hsdag,
        solution_rctree,
        solution_hsdag == solution_rctree,
        elapsed_hsdag,
        elapsed_rctree,
        elapsed_rctree / elapsed_hsdag * 100,
        hs_dag.amount_of_nodes_constructed,
        rc_tree.amount_of_nodes_constructed,
        rc_tree.amount_of_nodes_constructed /
        hs_dag.amount_of_nodes_constructed * 100,
        len(hs_dag.nodes),
        len(rc_tree.nodes),
        len(rc_tree.nodes) / len(hs_dag.nodes) * 100,
    )
    print(report)
    if render:
        if output_files_prefix:
            hs_dag.render(output_files_prefix + '_hsdag.gv')
            rc_tree.render(output_files_prefix + '_rctree.gv')
        else:
            hs_dag.render()
            rc_tree.render()
