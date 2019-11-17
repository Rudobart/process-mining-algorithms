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
        self.event_outcomes = self.footprint.node_outcomes
        self.flows = []




    def build_bpmn(self):
        self.add_nodes()
        self.add_start_events()
        self.add_parallels()
        self.add_gates()
        self.add_flows()
        print(self.node_ancestors)
        print(self.node_successors)
        print(self.succession)
        print(self.event_incomes)
        print(self.event_outcomes)
        print(self.flows)





        layouter.generate_layout(self.bpmn_graph)
        # Uncomment line below to get a simple view of created diagram
        #visualizer.visualize_diagram(self.bpmn_graph)
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
            self.flows.append((start_id,start_event_id))

    def add_parallels(self):
        parallels = self.footprint.parallels
        for parallel in parallels:
            [parallel_start, _] = self.bpmn_graph.add_parallel_gateway_to_diagram(self.process_id)
            [parallel_end, _] = self.bpmn_graph.add_parallel_gateway_to_diagram(self.process_id)
            for event in parallel:
                self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, parallel_start, event)
                self.flows.append((parallel_start, event))
                self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, parallel_end)
                self.flows.append((event,parallel_end))
                self.node_ancestors.setdefault(event, []).append(parallel_start)
                self.node_successors.setdefault(event, []).append(parallel_end)

    def add_gates(self):
        for event in self.event_incomes:
            if self.event_incomes[event] > 1:
                [exclusive_gate_id, _] = self.bpmn_graph.add_exclusive_gateway_to_diagram(self.process_id)
                self.node_ancestors.setdefault(event, []).append(exclusive_gate_id)

        for event in self.event_outcomes:
            if self.event_outcomes[event] > 1:
                [exclusive_gate_id, _] = self.bpmn_graph.add_exclusive_gateway_to_diagram(self.process_id)
                self.node_successors.setdefault(event, []).append(exclusive_gate_id)




    def add_flows(self):
        parallels = self.footprint.parallels
        for event in self.succession:
            if event in self.node_ancestors:
                if len(self.node_ancestors[event]) > 1:
                    for index, id in enumerate(self.node_ancestors[event]):
                        if index + 1 != len(self.node_ancestors[event]):
                           self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_ancestors[event][index+1], id)
                           self.flows.append((self.node_ancestors[event][index+1], id))
                if self.is_in_parallel(event, parallels) is False:
                    self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_ancestors[event][0], event)
                    self.flows.append((self.node_ancestors[event][0], event))

            if event in self.node_successors:
                if len(self.node_successors[event]) > 1:
                    for index, id in enumerate(self.node_successors[event]):
                        if index + 1 != len(self.node_successors[event]):
                           self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, id, self.node_successors[event][index+1])
                           self.flows.append((id, self.node_successors[event][index+1]))

                if self.is_in_parallel(event, parallels) is False:
                    self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, self.node_successors[event][0])
                    self.flows.append((event, self.node_successors[event][0]))

            for value in self.succession[event]:
                print(event, value, self.is_connected(event, value))
                if not self.is_connected(event, value):
                     if self.is_in_parallel(event, parallels) and self.event_incomes[event] == 1:
                             continue
                     if event in self.node_successors and value in self.node_ancestors:
                         self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_successors[event][-1], self.node_ancestors[value][-1])
                         self.flows.append((self.node_successors[event][-1], self.node_ancestors[value][-1]))

                     elif event in self.node_successors and value not in self.node_ancestors:
                         self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_successors[event][-1], value)
                         self.flows.append((self.node_successors[event][-1], value))

                     elif event not in self.node_successors and value in self.node_ancestors:
                         self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, self.node_ancestors[value][-1])
                         self.flows.append((event, self.node_ancestors[value][-1]))

                     elif event not in self.node_successors and value not in self.node_ancestors:
                         self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, value)
                         self.flows.append((event, value))

    def is_connected(self, source, target):
        availables= []
        availables.append(source)
        for ava in availables:
            for tuple in self.flows:
                if tuple[0] == ava and tuple[1] not in availables:
                    availables.append(tuple[1])


        if target in availables:
            return True
        return False







    def is_in_parallel(self, event, parallels):
        for parallel in parallels:
            if event in parallel:
                return True
        return False

    def current_parallel(self, event, value, parallels):
        for parallel in parallels:
            if event in parallel or value in parallel:
                return parallel
        return []






alpha = Alpha(log_list)
alpha.build_bpmn()
