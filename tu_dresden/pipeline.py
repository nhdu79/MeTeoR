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
import os

parser = argparse.ArgumentParser()
parser.add_argument("--facts", default="10000", type=str, help="Input the dataset path")
parser.add_argument("--rulepath", default="programs/p.txt", type=str, help="Input the program path")

"""
    Direct from the dataset:
    10000: Publication(ID16)@[1,9]
    20000: Publication(ID16)@[6,31]
    30000: Publication(ID16)@[31,41]
    40000: Publication(ID16)@[37,49]
    50000: Publication(ID16)@[14,24]
    60000: Publication(ID16)@[16,46]
    70000: Publication(ID16)@[16,29]
    80000: Publication(ID16)@[7,26]
    90000: Publication(ID16)@[17,26]
    100000: Publication(ID16)@[31,41]
"""

ds_facts = {
    "10000": "Publication(ID16)@[1,9]",
    "20000": "Publication(ID16)@[6,31]",
    "30000": "Publication(ID16)@[31,41]",
    "40000": "Publication(ID16)@[37,49]",
    "50000": "Publication(ID16)@[14,24]",
    "60000": "Publication(ID16)@[16,46]",
    "70000": "Publication(ID16)@[16,29]",
    "80000": "Publication(ID16)@[7,26]",
    "90000": "Publication(ID16)@[17,26]",
    "100000": "Publication(ID16)@[31,41]"
}


# parser.add_argument("--fact", default="Publication(ID16)@[1,9]",  type=str, help="Input a fact  you wanna check the entailment")

args = parser.parse_args()

nr_facts = args.facts
data_path_relative = f"output/{nr_facts}.txt"
current_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(current_path, data_path_relative)
D = load_dataset(data_path)

with open(args.rulepath) as file:
    rules = file.readlines()
    program = load_program(rules)

try:
    # fact = args.fact
    fact = ds_facts[args.facts]
    predicate, entity, interval = parse_str_fact(fact)
    fact = Atom(predicate, entity, interval)
except:
    raise ("The format you input is incorrect")

glassbox = True

def run():
    result = entailment_check_without_load(D, program, fact, glassbox=glassbox)
    if result == False:
        print("Materialisation: Not entailed")
        return False
    else:
        if glassbox:
            facts = []
            with open(data_path, 'r') as f:
                data = f.readlines()
                for line in data:
                    raw = line.strip()
                    if len(raw) > 0 and raw not in facts:
                        facts.append(line.strip())
            parser = HyperGraphParser(result, facts)
            parser.initialization()
            file_name = data_path_relative.split(".")[0]
            parser.write_to_file_as_json("{}.json".format(file_name))
        return True


start_time = time.perf_counter()
entailment = run()
end_time = time.perf_counter()
total_time = end_time - start_time
print("========= RESULT =========")
print("Total time: ", total_time)
# Write total time to result.txt, where each line contains number of facts : total time
with open("results.txt", "a") as f:
    f.write(f"{nr_facts} : {total_time}\n")
