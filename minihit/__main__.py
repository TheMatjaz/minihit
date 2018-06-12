#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .algcompare import solve_from_file

import sys

render = False
prune = False
sort = False
output_files_prefix = None
help_text = """{:s}
Usage:

python -m minihit input_file_name [--render [--output_files_prefix=PREFIX]] 
[--prune | --sort]

input_file_name       Path to the file containing conflict sets to parse.
render                Enables the generation a graphical representations of the 
                      algorithms without saving the output file, unless PREFIX
                      is specified.
output                Path and prefix of the output files.
prune                 Enables pruning of the generated DAGs (in doubt, set it).
                      Activating pruning disables sorting.
sort                  Sorts set of conflicts before starting the search for
                      minimal hitting sets.
                      Activating sorting disables pruning.
"""
if len(sys.argv) < 2:
    print(help_text.format('Illegal amount of arguments'))
    exit(1)
for argument in sys.argv[1:]:
    argument = str(argument).lower().strip().lstrip('-')
    if argument == 'render':
        render = True
    elif argument == 'sort':
        sort = True
        prune = False
    elif argument == 'prune':
        prune = True
        sort = False
    elif argument.startswith('output'):
        output_files_prefix = argument.split('=', 1)[1]
solve_from_file(sys.argv[1],
                render=True,
                output_files_prefix=output_files_prefix,
                prune=prune,
                sort=sort)
