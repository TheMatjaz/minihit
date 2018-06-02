Algorithm variable names
===============================================================================

HS-DAG
----------------------------------------

- D = HsDag, the DAG
- n_0 = HsDag().root, the root node
- CS = MinimalHittingsetProblem().conflict_sets
- ✓ = HsDagNode().is_ticked
- n = processed_node, the node to add to the DAG
- h(n) = new_node.path_from_root
- (In step 2) C_j = the first conflict set that does not share any conflict with the ones in new_node.label
- n' = other_node
- (In step 3) C_j = other_node.label
