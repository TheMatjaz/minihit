MiniHit: minimal hitting set solver in Python
==============================================================================

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE.md)
![Python Version](https://img.shields.io/pypi/pyversions/Django.svg)

A Python solver for the minimal hitting set problem commonly found as part of 
diagnosis problems.

MiniHit provides the following algorithms:

- [HS-DAG](http://www.cs.ru.nl/P.Lucas/teaching/KeR/Theorist/greibers-correctiontoreiter.pdf)
  by Raymond Reiter, later corrected by Russell Greiner, Barbara A. Smith and 
  Ralph W. Wilkerson
- [RC-Tree](http://www.ist.tugraz.at/pill/downloads/IWPD15_p5_preprint.pdf)
  by Ingo Pill and Thomas Quaritsch


Requirements
----------------------------------------

- You will need Python>=3.4.
- If you intend to use rendering functionality of the data structures
  created by the algorithms, then you'll need
  [Graphviz](https://graphviz.gitlab.io/download/). Install it 
  and make sure that the `dot` executable is in your `PATH` environment
  variable. Then install its Python wrapper with `pip install graphviz`.


Disclaimer
----------------------------------------

This package was written for academic purposes, so **performance was never
the main goal**. If you are willing to optimize it even further, open a
pull request! :)


Usage
----------------------------------------

### Package execution

```bash
# Get the help text if needed
python -m minihit --help

# Simple computation of minimal hitting sets with all algorithms
python -m minihit input.txt

# With enabled rendering
python -m minihit input.txt --render

# With enabled rendering and saving the output files with a prefix
python -m minihit input.txt --render --outprefix=/path/to/your/minimal_hitting_sets

# With enabled pruning
python -m minihit input.txt --prune

# With sorting and rendering
python -m minihit input.txt --sort --render
```
(on your system it may be called `python3` instead of `python`).

The content of `input.txt` file has to be formatted in one of the two following
syntaxes, which are equivalent
```
1,2,3|1,3,4|6,7  # This is a comment
|||1,1,1,1,2|  # This is the second malformatted problem with only a set {1,2}
```

```
[{1, 2, 3}, {1, 3, 4}, {6, 7}]  # This is written in Python syntax
[{1, 2}]  # it's easy to copy-paste Python code in the input.txt file.
```

**Note**: by default the set elements are integers, this can be configured
in the `ConflictSetsFileParser` constructor. In other usage methods,
the set elements could be anything.


### Simple comparison between algorithms

```python
>>> import minihit
>>> minihit.compare([{1, 2, 3}, {1, 3, 4}, {6, 7}])
Conflict sets: [{1, 2, 3}, {1, 3, 4}, {6, 7}]
HSDAG solution:   [{1, 6}, {1, 7}, {3, 6}, {3, 7}, {2, 4, 6}, {2, 4, 7}]
RC-Tree solution: [{1, 6}, {1, 7}, {3, 6}, {3, 7}, {2, 4, 6}, {2, 4, 7}]
Algorithm produce same result: True
HSDAG solution is correct:     True
RC-Tree solution is correct:   True
HSDAG runtime [s]:   0.000646
RC-Tree runtime [s]: 0.000375
HSDAG/RC-Tree runtime [%]: 172.219
HSDAG nodes constructed:   17
RC-Tree nodes constructed: 14
RC-Tree/HSDAG constructions [%]:  82.353
HSDAG nodes:   13
RC-Tree nodes: 12
RC-Tree/HSDAG nodes [%]:  92.308

# As mentioned above, other data types could be also used
>>> minihit.compare([{'alpha', 'beta'}, {'alpha', 'omega'}, {'epsilon'}])
```


### Direct solver usage

The solver classes you may want are subclasses of the 
`MinimalHittingsetProblem` class. In particular those are
`RcTree` and `HsDag`. Both share a common API.

```python
>>> import minihit

# Construct solver with set of conflicts. The methods shown below
# are exactly the same for the HsDag class as well.
>>> rctree = minihit.RcTree([{1, 2, 3}, {1, 3, 4}, {6, 7}])

# Run solver with optional pruning and sorting by cardinality before starting
# the tree construction. Runtime is returned
>>> elapsed_seconds = rctree.solve(prune=True, sort=False)

# Inspect the space complexity required
>>> rctree.amount_of_nodes_constructed
14

# Obtain the minimal hitting sets (as a generator)
>>> rctree.generate_minimal_hitting_sets()
<generator object HsDag.generate_minimal_hitting_sets at 0x107be96d0>

>>> list(rctree.generate_minimal_hitting_sets())
[{1, 6}, {1, 7}, {3, 6}, {3, 7}, {2, 4, 6}, {2, 4, 7}]

# Visualize the result, don't save output file
>>> rctree.render()

# Save output file
>>> rctree.render("/save/to/my/file")

# Solve again for the same set of conflicts
>>> rctree.solve()

# Solve for another set of conflicts
>>> rctree.list_of_conflicts = [{1, 2}, {3}]
>>> rctree.solve()

# Explore the generated DAG/Tree from the root (without revisiting nodes)
>>> for node in rctree.breadth_first_explore(rctree.root):
>>>     print(node)
```
