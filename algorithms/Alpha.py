from config import *
import bpmn_python.bpmn_diagram_layouter as layouter
import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram
from algorithms.utils import Footprint as footprint

class Alpha:
    def __init__(self, log):
        self.log = log
        self.footprint = footprint(self.log)
        self.succession = self.footprint.succession
        self.bpmn_graph = diagram.BpmnDiagramGraph()
        self.bpmn_graph.create_new_diagram_graph(diagram_name="alpha_alogrithm_bpmn")
        self.process_id = self.bpmn_graph.add_process_to_diagram()
        self.node_ancestors = {}
        self.node_successors = {}
        self.event_incomes = self.footprint.node_incomes
        self.event_outcomes = {}




    def build_bpmn(self):
        self.succession["d"].remove("b")
        self.add_nodes()
        self.add_start_events()
        self.add_parallels()
        self.add_gates()
        self.add_flows()
        print(self.node_ancestors)
        print(self.succession)
        print(self.event_incomes)





        layouter.generate_layout(self.bpmn_graph)
        # Uncomment line below to get a simple view of created diagram
        #visualizer.visualize_diagram(bpmn_graph)
        self.bpmn_graph.export_xml_file(output_directory, "alpha_algorithm.bpmn")




    def add_nodes(self):
        added_nodes = []
        for event in self.footprint.unique_events:
            if event not in added_nodes:
                self.bpmn_graph.add_task_to_diagram(self.process_id, task_name=event, node_id=event)


    def add_start_events(self):
        for start_event in self.footprint.start_events:
            [start_id, _] = self.bpmn_graph.add_start_event_to_diagram(self.process_id,start_event_definition="timer")
            start_event_id = start_event
            self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, start_id, start_event_id)

    def add_parallels(self):
        parallels = self.footprint.max_parallels()
        for parallel in parallels:
            [parallel_start, _] = self.bpmn_graph.add_parallel_gateway_to_diagram(self.process_id, gateway_name="parallel_start")
            [parallel_end, _] = self.bpmn_graph.add_parallel_gateway_to_diagram(self.process_id, gateway_name="parallel end")
            for event in parallel:
                self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, parallel_start, event)
                self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, parallel_end)
                self.node_ancestors.setdefault(event, []).append(parallel_start)
                self.node_successors.setdefault(event, []).append(parallel_end)

    def add_gates(self):
        for event in self.event_incomes:
            if self.event_incomes[event] > 1:
                [exclusive_gate_id, _] = self.bpmn_graph.add_exclusive_gateway_to_diagram(self.process_id)
                self.node_ancestors.setdefault(event, []).append(exclusive_gate_id)

    def add_flows(self):
        for event in self.succession.keys():
            if event in self.node_ancestors:
                if len(self.node_ancestors[event]) > 1:
                    for index, id in enumerate(self.node_ancestors[event]):
                        if index + 1 != len(self.node_ancestors[event]):
                           self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_ancestors[event][index+1], id)
                if self.is_in_parallel(event, self.footprint.max_parallels()) is False:
                    self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_ancestors[event][0], event)
            else:






    def is_in_parallel(self, event, parallels):
        for parallel in parallels:
            if event in parallel:
                return True
        return False






alpha = Alpha(log_list)
alpha.build_bpmn()