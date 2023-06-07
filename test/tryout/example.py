from meteor_reasoner.utils.entailment_checker import entailment_check

data = ["B(a)@[1,2]", "C(a)@1"]
program = ["A(X):- Boxminus[1,1]Boxplus[1,2]B(X), C(X)"]
fact = "A(a)@1"

# data = ["A(a)@1", "C(a)@1"]
# program = ["D(X):- Boxminus[1,1]A(X), B(X)", "B(X):- Boxminus[1,1]C(X)"]
# fact = "D(a)@2"

# current_path = os.path.dirname(os.path.realpath(__file__))
# program_path= os.path.join(current_path, "../data/finite_program.txt")
# data_path = os.path.join(current_path, "../data/finite_program.txt")
# fact = ""

result = entailment_check(data, program, fact, glassbox=True)

breakpoint()

# HEAD ~ "Boxplus[1,2](A(a))@[6,7]"
# we need to add A(a)@[7,9] to D to make HEAD true
# = >>> reverse_apply(HEAD, D)
