from meteor_reasoner.utils.entailment_checker import entailment_check

data = ["C(a)@1","B(a)@[1,2]","C(a)@2"]
program = ["A(X):-B(X), C(X)"]
fact = "A(a)@1"

result = entailment_check(data, program, fact, glassbox=True)

breakpoint()

# HEAD ~ "Boxplus[1,2](A(a))@[6,7]"
# we need to add A(a)@[7,9] to D to make HEAD true
# = >>> reverse_apply(HEAD, D)
