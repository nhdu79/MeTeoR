from meteor_reasoner.graphutil.graph_strengthening import *
from meteor_reasoner.graphutil.multigraph import *
from meteor_reasoner.utils.loader import load_program

import os
current_path = os.path.dirname(os.path.realpath(__file__))
program_path = os.path.join(current_path, "data/finite_program.txt")

###
# DNH
# Testing acyclicity, probably for the Automata
###

# MTL-acyclic must be a finitely materialisable program,but not every finitely materialisable program is MTL-acyclic
def test_finite_materialisability():
    rules = load_program(program_path)
    rules = transformation(rules)
    pairs = construct_pair(rules)
    G = TemporalDependencyGraph()
    for pair in pairs:
        G.add_edge(pair[0], pair[1], [pair[2], pair[3]])

    print("The input program is MTL-acyclic:", G.is_cyclic())

test_finite_materialisability()
