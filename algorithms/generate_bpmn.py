
from config import log_list
from algorithms.AlphaMiner import AlphaMiner
from algorithms.HeuristicMiner import HeuristicMiner
from algorithms.SplitMiner import SplitMiner

if __name__ == '__main__':
    alpha_miner = AlphaMiner(log_list)
    heuristic_miner = HeuristicMiner(log_list)
    split_miner = SplitMiner(log_list)

    alpha_miner.build_bpmn()
    heuristic_miner.build_bpmn()
    split_miner.build_bpmn()

    print("stworzono diagramy")

