from meteor_reasoner.utils.entail_check import entail
from meteor_reasoner.utils.operate_dataset import *
from meteor_reasoner.utils.hypergraph_parser import HyperGraphParser
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.materialization.coalesce import *
from meteor_reasoner.materialization.index_build import *
from meteor_reasoner.utils.parser import parse_str_fact
from meteor_reasoner.materialization.materialize import materialize
import copy

# data = ["B(a)@[0,1]", "C(a)@1"]
# data = ["A(a)@[0,2]", "A(a)@[1,3]", "A(a)@[4,5)", "A(a)@5", "A(a)@(5,6)"]
data = ["B(a)@0"]
program = ["A(X):- Boxminus[1,1]Boxplus[1,1]B(X)"]
fact = "A(a)@0"

predicate, entity, interval = parse_str_fact(fact)
F = Atom(predicate, entity, interval)
graph = []
facts = copy.deepcopy(data)

D = load_dataset(data)
entail(F, D, graph=graph)
coalescing_d(D, graph=graph)
D_index = build_index(D)
program = load_program(program)

def run():
    if entail(F, D, graph=graph):
        return True
    else:
        while True:
            flag = materialize(D, rules=program, mode="naive", K=1, graph=graph, fakt=F)
            if entail(F, D, graph=graph):
                return True
            else:
                if flag:
                    return False

# program = ["Boxplus[1,1]A(X):- B(X)"]
# fact = "A(a)@2"

# data = ["B(a)@[1,2]", "C(a)@1", "C(a)@10"]
# program = ["Boxplus[1,1]Boxminus[1,1]A(X):- C(X)"]
# program = ["Boxminus[1,1]A(X):- Boxminus[1,1]Boxplus[1,2]B(X), C(X)"]
# fact = "A(a)@1"

# data = ["B(a)@[1,2]", "C(a)@1"]
# program = ["A(X):- Boxminus[1,1]Boxplus[1,2]B(X), C(X)"]

entailment = run()
if entailment:
    parser = HyperGraphParser(graph, facts)
    parser.initialization()

breakpoint()

# HEAD ~ "Boxplus[1,2](A(a))@[6,7]"
# we need to add A(a)@[7,9] to D to make HEAD true
# = >>> reverse_apply(HEAD, D)
