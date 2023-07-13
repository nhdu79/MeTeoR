from meteor_reasoner.materialization.index_build import *
from meteor_reasoner.materialization.coalesce import *
from meteor_reasoner.utils.loader import load_dataset, load_program
from meteor_reasoner.utils.parser import parse_str_fact
from meteor_reasoner.classes import *
from meteor_reasoner.utils.entail_check import entail
from meteor_reasoner.materialization.materialize import materialize
import random
import time
import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("--facts", default="10000", type=str, help="Input the dataset path")
parser.add_argument("--rulepath", default="programs/p.txt", type=str, help="Input the program path")

parser.add_argument("--iteration", default=5, type=int, help="Input the iteration times")

args = parser.parse_args()

nr_facts = args.facts
iter = args.iteration

data_path_relative = f"output/{nr_facts}.txt"
current_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(current_path, data_path_relative)
D = load_dataset(data_path)

coalescing_d(D)
D_index = build_index(D)

with open(args.rulepath) as file:
    rules = file.readlines()
    program = load_program(rules)


while iter > 0:
    materialize(D, rules=program, mode="naive", K=1)
    iter -= 1

selected_facts = []
keys = list(D['Scientist'].keys())
sampled_keys = random.sample(keys, 5)

for key in sampled_keys:
    intervals = D['Scientist'][key]
    interval = random.choice(intervals)
    fact = Atom("Scientist", entity=key, interval=interval)
    selected_facts.append(fact.__str__())

# Write the selected facts to file
with open(f"data/T4_{nr_facts}.txt", "w") as file:
    file.write("\n".join(selected_facts))





