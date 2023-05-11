from meteor_reasoner.canonical.utils import find_periods
from meteor_reasoner.canonical.canonical_representation import CanonicalRepresentation
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.utils.parser import parse_str_fact
from meteor_reasoner.classes.atom import Atom
from meteor_reasoner.canonical.utils import fact_entailment

class Glassbox:
    def __init__(self, data, program, K=100, mode="naive"):
        self.data = data
        self.program = program
        self.mode = mode
        self.graph = {
            "vertices": [],
            "edges": [],
        }
        self.K = K

    def initialize(self):
        if self.mode == "naive":
            self.naive_materialize()
        elif self.mode == "seminaive":
            self.seminaive_materialize()
        else:
            raise Exception("Invalid mode")

    def naive_materialize(self):
        k = 0
        D_index = build_index(D)
        delta_old = D

        while k < self.K:
            k += 1
            delta_new = naive_immediate_consequence_operator(rules, D, D_index)
            if logger is not None:
                delta_old = defaultdict(lambda: defaultdict(list))
                fixpoint = seminaive_combine(D, delta_new, delta_old, D_index)
                coalescing_d(delta_new)
                number_of_redundant_facts = calculate_redundancy(delta_new, delta_old)
                total_number = 0
                for predicate in D:
                    for entity in D[predicate]:
                        total_number += len(D[predicate][entity])
                logger.info("Iteration={}, t={}, D={}, n={}".format(k, time.time() - start_time - calc_time, total_number, number_of_redundant_facts))
            else:
                fixpoint = naive_combine(D, delta_new, D_index)
            if fixpoint:
                return True

        return False










