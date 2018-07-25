#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
High-level comparator between the HSDAG and RC-Tree algorithms.
"""

from typing import List

from . import getconflicts, hsdag, rctree


def compare_from_file(input_file_name, render: bool = False,
                      output_files_prefix: str = None, prune: bool = True,
                      sort: bool = False):
    """
    Executes both HSDAG and RC-Tree on the same set of conflicts read from
    a file, comparing runtime and memory required.

    Args:
        input_file_name: file containing iterables of conflicts (sets of
            anything) to find the minimal hitting sets for.
            The format has to be as specified in the `README.md`.
        render: set to True to display the constructed DAG and tree by the
            algorithms.
        output_files_prefix: prefix of the filenames to create. Set to None
            to avoid storing files.
        prune: set to True to activate of the pruning feature of both
            algorithms.
        sort: set to True to sort the conflicts by cardinality before executing
            the algorithms. This deactivates pruning, as it's no longer
            required.

    Returns:
        None. The output is printed to STDOUT in human readable format.
    """
    parser = getconflicts.ConflictSetsFileParser()
    parser.parse(input_file_name)
    for line, list_of_conflicts in parser.sets_by_line.items():
        print("------\nLine: {:d}".format(line))
        compare(list_of_conflicts, render, output_files_prefix, prune, sort)


def compare(list_of_conflicts: List[set], render: bool = False,
            output_files_prefix: str = None, prune: bool = True,
            sort: bool = False):
    """
    Executes both HSDAG and RC-Tree on the same set of conflicts,
    comparing runtime and memory required.

    Args:
        list_of_conflicts: iterable of conflicts (sets of anything) to find
            the minimal hitting sets for. This input list is never modified.
        render: set to True to display the constructed DAG and tree by the
            algorithms.
        output_files_prefix: prefix of the filenames to create. Set to None
            to avoid storing files.
        prune: set to True to activate of the pruning feature of both
            algorithms.
        sort: set to True to sort the conflicts by cardinality before executing
            the algorithms. This deactivates pruning, as it's no longer
            required.

    Returns:
        None. The output is printed to STDOUT in human readable format.
    """
    hs_dag = hsdag.HsDag(list_of_conflicts)
    elapsed_hsdag = hs_dag.solve(prune=prune, sort=sort)
    solution_hsdag = list(hs_dag.generate_minimal_hitting_sets())
    frozen_solution_hsdag = set(map(frozenset, solution_hsdag))
    hs_dag_solution_is_correct = hs_dag.verify()
    rc_tree = rctree.RcTree(list_of_conflicts)
    elapsed_rctree = rc_tree.solve(prune=prune, sort=sort)
    solution_rctree = list(rc_tree.generate_minimal_hitting_sets())
    frozen_solution_rctree = set(map(frozenset, solution_rctree))
    rc_tree_solution_is_correct = rc_tree.verify()
    report = \
        "Conflict sets: {:}\n" \
        "HSDAG solution:   {:}\n" \
        "RC-Tree solution: {:}\n" \
        "Algorithm produce same result: {:}\n" \
        "HSDAG solution is correct:     {:}\n" \
        "RC-Tree solution is correct:   {:}\n" \
        "HSDAG runtime [s]:   {:f}\n" \
        "RC-Tree runtime [s]: {:f}\n" \
        "HSDAG/RC-Tree runtime [%]: {:7.3f}\n" \
        "HSDAG nodes constructed:   {:d}\n" \
        "RC-Tree nodes constructed: {:d}\n" \
        "RC-Tree/HSDAG constructions [%]: {:7.3f}\n" \
        "HSDAG nodes:   {:d}\n" \
        "RC-Tree nodes: {:d}\n" \
        "RC-Tree/HSDAG nodes [%]: {:7.3f}".format(
            list_of_conflicts,
            solution_hsdag,
            solution_rctree,
            frozen_solution_hsdag == frozen_solution_rctree,
            hs_dag_solution_is_correct,
            rc_tree_solution_is_correct,
            elapsed_hsdag,
            elapsed_rctree,
            elapsed_hsdag / elapsed_rctree * 100,
            hs_dag.amount_of_nodes_constructed,
            rc_tree.amount_of_nodes_constructed,
            rc_tree.amount_of_nodes_constructed /
            hs_dag.amount_of_nodes_constructed * 100,
            len(list(hs_dag.breadth_first_explore(hs_dag.root))),
            len(list(rc_tree.breadth_first_explore(rc_tree.root))),
            len(list(rc_tree.breadth_first_explore(rc_tree.root)))
            / len(list(hs_dag.breadth_first_explore(hs_dag.root))) * 100,
        )
    print(report)
    if render:
        if output_files_prefix:
            hs_dag.render(output_files_prefix + '_hsdag')
            rc_tree.render(output_files_prefix + '_rctree')
        else:
            hs_dag.render()
            rc_tree.render()
