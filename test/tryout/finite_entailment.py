from meteor_reasoner.utils.entailment_checker import entailment_check
import os

data = ["NotInf(a)@30, NotVacc(a)@[0, 365]"]
current_path = os.path.dirname(os.path.realpath(__file__))
program_path= os.path.join(current_path, "../data/finite_program.txt")
fact = "Susc(a)@30"

entailment_check(data, program_path, fact)
