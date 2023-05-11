"""
Materialization of a program
"""
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.materialization.materialize import *
import os

# data = ["A(a)@1", "B(a)@[1,2]", "C@(1,2]"]
# program = ["A(X):-Diamondminus[1,2]A(X)", "D(X):- Boxminus[1,2]A(X), B(X)Since[1,2]C"]
#

data = ["NotVacc(a)@[2,3], NotInf(a)@2"]
current_path = os.path.dirname(os.path.realpath(__file__))
program = os.path.join(current_path, "../data/finite_program.txt")

D = load_dataset(data)
Program = load_program(program)

flag = materialize(D, Program, mode="naive", K=1)
# flag = materialize(D, Program, mode="seminaive", K=10)
# flag = materialize(D, Program, mode="opt", K=10)
print_dataset(D)
