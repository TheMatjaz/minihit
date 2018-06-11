#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .algcompare import solve_from_file

import sys

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
Usage: python minihit input_file_name [--render [--output_files_prefix=PREFIX]]

input_file_name: path to the file containing conflict sets to parse
render: enables the generation a graphical representations of the 
        algorithms without saving the output file, unless PREFIX is specified
output_files_prefix: path and prefix of the output files"""
    print(help_text)
    exit(1)
