from meteor_reasoner.utils.entailment_checker import entailment_check
from proof_extractor.hypergraph_parser import HyperGraphParser

data = ["B(a)@[0,1]", "C(a)@1"]
program = ["A(X):- B(X)Since[1,2]Boxplus[1,1]C(X)"]
fact = "A(a)@1"

# program = ["Boxplus[1,1]A(X):- B(X)"]
# fact = "A(a)@2"

# data = ["B(a)@[1,2]", "C(a)@1", "C(a)@10"]
# program = ["Boxplus[1,1]Boxminus[1,1]A(X):- C(X)"]
# program = ["Boxminus[1,1]A(X):- Boxminus[1,1]Boxplus[1,2]B(X), C(X)"]
# fact = "A(a)@1"

# data = ["B(a)@[1,2]", "C(a)@1"]
# program = ["A(X):- Boxminus[1,1]Boxplus[1,2]B(X), C(X)"]

result = entailment_check(data, program, fact, glassbox=True)
parser = HyperGraphParser(result, data)
parser.initialization()

parser.write_to_file_as_json("test.json")

breakpoint()

# HEAD ~ "Boxplus[1,2](A(a))@[6,7]"
# we need to add A(a)@[7,9] to D to make HEAD true
# = >>> reverse_apply(HEAD, D)
