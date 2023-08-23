from meteor_reasoner.utils.entailment_checker import entailment_check
from meteor_reasoner.utils.hypergraph_parser import HyperGraphParser
import os

# case = 0
# fact = "Q@0.5"
# case = 3
# fact = "A(a)@3"
# case = 4
# fact = "A(a)@4"
# case = 5
# fact = "A(a)@10"
# case = 6
# fact = "A(a)@10"
# case = 7
# fact = "A(a)@26.5"
# case = 8
# fact = "A(a)@4"
# case = 9
# fact = "NoSymptoms(charlie)@100"
case = 15
fact = "A(a,b)@0"


current_path = os.path.dirname(os.path.realpath(__file__))
program_path= os.path.join(current_path, "../data/case_{}_program.txt".format(case))
data_path = os.path.join(current_path, "../data/case_{}_dataset.txt".format(case))


result = entailment_check(data_path, program_path, fact, glassbox=True)
facts = []
with open(data_path, 'r') as f:
    data = f.readlines()
    for line in data:
        if len(line.strip()) > 0:
            facts.append(line.strip())

parser = HyperGraphParser(result, facts)
parser.initialization()

breakpoint()
# parser.write_to_file_as_json("test_{}.json".format(case))
