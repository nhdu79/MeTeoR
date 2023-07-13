from meteor_reasoner.utils.hypergraph_parser import HyperGraphParser
from meteor_reasoner.materialization.index_build import *
from meteor_reasoner.materialization.coalesce import *
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.utils.parser import parse_str_fact
from meteor_reasoner.classes import *
from meteor_reasoner.utils.entail_check import entail
from meteor_reasoner.materialization.materialize import materialize
import time
import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("--facts", default="10000", type=str, help="Input the dataset path")
parser.add_argument("--rulepath", default="programs/p.txt", type=str, help="Input the program path")
parser.add_argument("--glassbox", default="1", type=str, help="Do Glassbox tracing")

args = parser.parse_args()

nr_facts = args.facts

data_path_relative = f"output/{nr_facts}.txt"
current_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(current_path, data_path_relative)
D = load_dataset(data_path)

coalescing_d(D)
D_index = build_index(D)

with open(args.rulepath) as file:
    rules = file.readlines()
    program = load_program(rules)

try:
    fact_path = f"data/T4_{nr_facts}.txt"
    with open(fact_path, "r") as file:
        fact = file.readlines()[0].strip()

    predicate, entity, interval = parse_str_fact(fact)
    F = Atom(predicate, entity, interval)
except:
    raise Exception("The format you input is incorrect")

glassbox = args.glassbox
if glassbox == "1":
    graph = []
    facts = []
    with open(data_path, 'r') as f:
        data = f.readlines()
        for line in data:
            raw = line.strip()
            if len(raw) > 0 and raw not in facts:
                facts.append(line.strip())
else:
    graph = None
    print("The graph is None")
fixpoint = False


def run():
    if entail(F, D, graph=graph):
        return True
    else:
        while True:
            flag = materialize(D, rules=program, mode="naive", K=1, graph=graph)
            if entail(F, D, graph=graph):
                return True
            else:
                if flag:
                    return False

start_time = time.perf_counter()
entailment = run()

if glassbox == "1" and entailment:
    parser = HyperGraphParser(graph, facts)
    parser.initialization()
    file_name = data_path_relative.split(".")[0]
    # parser.write_to_bash()
    parser.write_to_file_as_json("{}.json".format(file_name))

end_time = time.perf_counter()
total_time = end_time - start_time
print("========= RESULT =========")
print("Total time: ", total_time)

if glassbox == "1":
    with open("trace_time.txt", "a") as f:
        f.write(f"{nr_facts} : {total_time}\n")
