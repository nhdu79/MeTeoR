from meteor_reasoner.utils.entailment_checker import entailment_check

data = ["A(a)@1", "B(a)@[1,2]", "C@(1,2]"]
program = ["A(X):-Diamondminus[1,2]A(X)", "D(X):- Boxminus[1,2]A(X), B(X)Since[1,2]C"]
fact = "A(a)@10"

result = entailment_check(data, program, fact, glassbox=True)

breakpoint()
