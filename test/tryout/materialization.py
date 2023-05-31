"""
Materialization of a program
"""
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.materialization.materialize import *
import os

data = ["A(a)@1", "B(a)@[1,2]", "C@(1,2]"]
program = ["A(X):-Diamondminus[1,2]A(X)", "D(X):- Boxminus[1,2]A(X), B(X)Since[1,2]C"]

D = load_dataset(data)
Program = load_program(program)

flag = materialize(D, Program, mode="naive", K=2)
# flag = materialize(D, Program, mode="seminaive", K=10)
# flag = materialize(D, Program, mode="opt", K=10)
print_dataset(D)
