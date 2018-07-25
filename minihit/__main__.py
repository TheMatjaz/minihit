#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parses the command line arguments when executing the package as a whole
and passes them to `algcompare.compare_from_file()`.
"""

from .algcompare import compare_from_file

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
outprefix             Path and prefix of the output files.
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
    if argument in ('h', 'help'):
        print(help_text.format('Minihit'))
        exit(0)
    elif argument == 'render':
        render = True
    elif argument == 'sort':
        sort = True
        prune = False
    elif argument == 'prune':
        prune = True
        sort = False
    elif argument.startswith('outprefix'):
        output_files_prefix = argument.split('=', 1)[1]
compare_from_file(sys.argv[1],
                  render=render,
                  output_files_prefix=output_files_prefix,
                  prune=prune,
                  sort=sort)
