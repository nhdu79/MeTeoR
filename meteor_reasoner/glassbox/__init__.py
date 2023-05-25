from meteor_reasoner.canonical.utils import find_periods
from meteor_reasoner.canonical.canonical_representation import CanonicalRepresentation
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.utils.parser import parse_str_fact
from meteor_reasoner.classes.atom import Atom
from meteor_reasoner.canonical.utils import fact_entailment
from meteor_reasoner.utils.operate_dataset import print_dataset

class Glassbox:
    def __init__(self, data, program, fact):
        self.fact = fact
        self.data = data
        self.program = program
        self.logs = []

    def initialize(self):
        self.D = load_dataset(self.data)
        self.Program = load_program(self.program)
        self.CR = CanonicalRepresentation(self.D, self.Program)
        self.CR.initialize()
        predicate, entity, interval = parse_str_fact(fact)
        self.FAKT = Atom(predicate, entity, interval)

    def check_for_entailment(self):
        self.initialize()
        D1, common, varrho_left, left_period, left_len, varrho_right, right_period, right_len = find_periods(self.CR)

        if varrho_left is None and varrho_right is None:
            print("This program is finitely materialisable for this dataset.")
            print_dataset(D1)
        else:
            if varrho_left is not None:
                print("left period:", str(varrho_left))
                for key, values in left_period.items():
                    print(str(key), [str(val) for val in values])
            else:
                print("left period:", "[" + str(self.CR.base_interval.left_value - self.CR.w) + "," + str(self.CR.base_interval.left_value), ")")

            if varrho_right is not None:
                print("right period:", str(varrho_right))
                for key, values in right_period.items():
                    print(str(key), [str(val) for val in values])
            else:
                print("right period:", "(" + str(self.CR.base_interval.right_value), "," +  str(self.CR.base_interval.right_value + self.CR.w) + "]")

        print("Entailment:", fact_entailment(D1, self.FAKT, common, left_period, left_len, right_period, right_len))

