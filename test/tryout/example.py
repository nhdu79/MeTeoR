from meteor_reasoner.utils.entailment_checker import entailment_check

data = ["C(a)@1","B(a)@1","B(b)@2","C(b)@2"]
program = ["A(X):-B(X), C(X)"]
fact = "A(a)@1"

entailment_check(data, program, fact)
