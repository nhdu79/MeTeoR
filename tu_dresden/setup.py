from meteor_reasoner.utils.entailment_checker import entailment_check_without_load
from meteor_reasoner.utils.hypergraph_parser import HyperGraphParser
from meteor_reasoner.materialization.index_build import *
from meteor_reasoner.materialization.coalesce import *
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.utils.parser import parse_str_fact
from meteor_reasoner.classes import *
import time
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--datapath", default="data/lubm.json", type=str, help="Input the dataset path")
parser.add_argument("--rulepath", default="programs/p.txt", type=str, help="Input the program path")
parser.add_argument("--fact", default="a1:Publication(http://www.department0.university0.edu/associateprofessor3/publication7)@[0,7]",  type=str, help="Input a fact  you wanna check the entailment")

args = parser.parse_args()

with open(args.datapath) as file:
    D = defaultdict(lambda: defaultdict(list))
    data = json.load(open(args.datapath))
    for predicate in data:
        for entry in data[predicate]:
            for entity, interval_dict in entry.items():
                interval = Interval(decimal.Decimal(interval_dict["left_value"]),
                                    decimal.Decimal(interval_dict["right_value"]),
                                    decimal.Decimal(interval_dict["left_open"]),
                                    decimal.Decimal(interval_dict["right_open"]))

                D[predicate][tuple([Term(name) for name in entity.split(",")])].append(interval)


with open(args.rulepath) as file:
    rules = file.readlines()
    program = load_program(rules)


try:
    fact = args.fact
    predicate, entity, interval = parse_str_fact(fact)
    fact = Atom(predicate, entity, interval)
except:
    raise ("The format you input is incorrect")


def run():
    result = entailment_check_without_load(D, program, fact, glassbox=False)
    if result == False:
        print("Materialisation: Not entailed")
        return False
    else:
        parser = HyperGraphParser(result, data)
        parser.initialization()
        parser.write_to_file_as_json("test.json")
        return True


start_time = time.perf_counter()
entailment = run()
end_time = time.perf_counter()
total_time = end_time - start_time
print("========= RESULT =========")
print("Total time: ", total_time)


