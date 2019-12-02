import unittest

import bpmn_python.bpmn_diagram_layouter as layouter
import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram
from config import log_list
from algorithms.Alpha import Alpha
from algorithms.HeuristicMiner import HeuristicMiner

if __name__ == '__main__':
   # alpha = Alpha(log_list)
    heuristic_miner = HeuristicMiner(log_list)
    heuristic_miner.build_bpmn()