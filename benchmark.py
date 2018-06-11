#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from typing import List

import minihit


def solve_from_file(input_file_name, render: bool = False,
                    output_files_prefix: str = None):
    parser = minihit.fileload.ConflictSetsFileParser()
    parser.parse(input_file_name)
    for line, conflict_sets in parser.sets_by_line.items():
        print("Line: {:d}".format(line))
        solve(conflict_sets, render, output_files_prefix)


def solve(conflict_sets: List[set], render: bool = False,
          output_files_prefix: str = None):
    hsdag = minihit.hsdag.HsDag(conflict_sets)
    elapsed_hsdag = hsdag.solve()
    solution_hsdag = list(hsdag.generate_minimal_hitting_sets())
    rctree = minihit.rctree.RcTree(conflict_sets)
    elapsed_rctree = rctree.solve()
    solution_rctree = list(rctree.generate_minimal_hitting_sets())
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
        hsdag.amount_of_nodes_constructed,
        rctree.amount_of_nodes_constructed,
        hsdag.amount_of_nodes_constructed /
        rctree.amount_of_nodes_constructed,
    )
    print(report)
    if render:
        if output_files_prefix:
            hsdag.render(output_files_prefix + '_hsdag.gv')
            rctree.render(output_files_prefix + '_rctree.gv')
        else:
            hsdag.render()
            rctree.render()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        solve_from_file(sys.argv[1], render=False)
    elif len(sys.argv) == 3 and sys.argv[2] == '--render':
        solve_from_file(sys.argv[1], render=True)
    elif (len(sys.argv) == 4 and sys.argv[2] == '--render'
          and sys.argv[3].startswith('--output_files_prefix=')):
        output_files_prefix = sys.argv[3].replace('--output_files_prefix=', '')
        solve_from_file(sys.argv[1], render=True,
                        output_files_prefix=output_files_prefix)
    else:
        help_text = """Unknown parameters
Usage: {0:s} input_file_name [--render [--output_files_prefix=PREFIX]]

input_file_name: path to the file containing conflict sets to parse
render: enables the generation a graphical representations of the algorithms
        without saving the output file, unless PREFIX is specified
output_files_prefix: path and prefix of the output files""".format(sys.argv[0])
        print(help_text)
        exit(1)
