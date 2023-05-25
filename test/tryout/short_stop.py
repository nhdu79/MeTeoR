from meteor_reasoner.utils.entailment_checker import entailment_check
import os

current_path = os.path.dirname(os.path.realpath(__file__))
program_path= os.path.join(current_path, "../data/short_stop.txt")
data_path = os.path.join(current_path, "../data/s1.txt")

fact = "ShortStop(veh6)@[3,3]"

result = entailment_check(data_path, program_path, fact, glassbox=True)

stuff = {
        'vertex': ['ShortStop(veh6)@[3,3]'],
        'edge': 'ShortStop(V):-NotPos(V),Boxminus[1,1]Pos(V),Boxminus[2,2]NotPos(V)',
        'parents': ['NotPos(veh6)@[1,1]', 'NotPos(veh6)@[3,3]', 'NotPos(veh6)@[4,4]', 'Pos(veh6)@[3,3]', 'NotPos(veh6)@[3,3]', 'NotPos(veh6)@[5,5]', 'NotPos(veh6)@[6,6]']
        }

breakpoint()
