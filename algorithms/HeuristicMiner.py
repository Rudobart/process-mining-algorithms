from config import *
import bpmn_python.bpmn_diagram_layouter as layouter
import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram
from algorithms.algorithms_utils import Footprint as footprint

class HeuristicMiner:
    def __init__(self, log):
        self.algorithm_name = "heuristic"
        self.log = log
        self.footprint = footprint(self.log, self.algorithm_name)
        self.succession = self.footprint.succession
        self.bpmn_graph = diagram.BpmnDiagramGraph()
        self.bpmn_graph.create_new_diagram_graph(diagram_name="heuristic_miner_bpmn")
        self.process_id = self.bpmn_graph.add_process_to_diagram()
        self.node_ancestors = {}
        self.node_successors = {}
        self.event_incomes = []
        self.event_outcomes = []
        self.flows = []
        self.frequency = []
        self.significance = []
        self.long_relations_frequency = []
        self.long_relations_significance = []
        self.calculate_significance()
        self.calculate_long_significance()
        self.significance_threshhold = 0.0
        self.one_loop_threshhold = 0.0


    def count_frequency(self):
        for i in self.footprint.unique_events:
            self.frequency.append([i, dict.fromkeys([w for w in self.footprint.unique_events], 0)])
            for trace in self.log:
                for i, event in enumerate(trace):
                    if i+1 != len(trace):
                        self.increment_freq(event, trace[i+1], self.frequency)

    def increment_freq(self, event, value, dicts):
        for freq_dict in dicts:
            if freq_dict[0] == event:
                freq_dict[1][value] += 1



    def return_dict_value(self, event, value, dicts):
        for freq_dict in dicts:
            if freq_dict[0] == event:
                return freq_dict[1][value]

    def sum_freq(self, event):
        sum = 0
        for trace in self.log:
            for event2 in trace:
                if event == event2:
                    sum += 1
        return sum

    def calculate_significance(self):
        self.count_frequency()
        for i in self.footprint.unique_events:
            self.significance.append([i, dict.fromkeys([w for w in self.footprint.unique_events], 0)])
        for freq_dict in self.frequency:
            event = freq_dict[0]
            for value in freq_dict[1]:
                a = self.return_dict_value(event, value, self.frequency)
                b = self.return_dict_value(value, event, self.frequency)
                for sign_dict in self.significance:
                    if sign_dict[0] == event:
                        if(event == value):
                            sign_dict[1][value] = (a) / (a + 1)
                        else:
                             sign_dict[1][value] = (a - b) / (a + b + 1)

    def count_long_frequency(self):
        for i in self.footprint.unique_events:
            self.long_relations_frequency.append([i, dict.fromkeys([w for w in self.footprint.unique_events], 0)])
        for trace in self.log:
            for i in range(len(trace)):
                for j in range(i+1, len(trace) - 1):
                    self.increment_freq(trace[i], trace[j], self.long_relations_frequency)


    def calculate_long_significance(self):
        self.count_long_frequency()
        for i in self.footprint.unique_events:
            self.long_relations_significance.append([i, dict.fromkeys([w for w in self.footprint.unique_events], 0)])
        for freq_dict in self.long_relations_frequency:
            event = freq_dict[0]
            for value in freq_dict[1]:
                a = self.return_dict_value(event, value, self.long_relations_frequency)
                b = self.sum_freq(event)
                for sign_dict in self.long_relations_significance:
                    if sign_dict[0] == event:
                        sign_dict[1][value] = a / (b + 1)



    def build_bpmn(self):
        self.add_nodes()
        self.add_start_events()
        self.add_parallels()
        self.remove_parallel_incomes_outcomes()
        self.event_incomes = self.footprint.count_node_incomes(self.succession, self.footprint.parallels)
        self.event_outcomes = self.footprint.count_node_outcomes(self.succession,self.footprint.parallels)
        self.add_gates()
        self.add_flows()
        self.add_end_events()
        # print("ancestors: ", self.node_ancestors)
        # print("successors: ", self.node_successors)
        # print("succession:", self.succession)
        # print("incomes: ", self.event_incomes)
        # print("outcomes: ",self.event_outcomes)
        # print("flows: ",self.flows)
        # print("log: ",self.log)
        # print("frequency", self.frequency)
        # print("significance: ", self.significance)





    #    layouter.generate_layout(self.bpmn_graph)
        # Uncomment line below to get a simple view of created diagram
        #visualizer.visualize_diagram(self.bpmn_graph)
        self.bpmn_graph.export_xml_file(output_directory, "heuristic_miner.bpmn")




    def add_nodes(self):
        added_nodes = []
        for event in self.footprint.unique_events:
            if event not in added_nodes:
                self.bpmn_graph.add_task_to_diagram(self.process_id, task_name=event, node_id=event)


    def add_start_events(self):
        for start_event in self.footprint.start_events:
            [start_id, _] = self.bpmn_graph.add_start_event_to_diagram(self.process_id)
            start_event_id = start_event
            self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, start_id, start_event_id)
            self.flows.append((start_id,start_event_id))

    def add_end_events(self):
        for end_event in self.footprint.end_events:
            [end_id, _] = self.bpmn_graph.add_end_event_to_diagram(self.process_id)
            self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, end_event, end_id)
            self.flows.append((end_event, end_id))





    def add_parallels(self):
        parallels = self.footprint.parallels
        event_count = {}
        for parallel in parallels:
            [parallel_start, _] = self.bpmn_graph.add_parallel_gateway_to_diagram(self.process_id)
            [parallel_end, _] = self.bpmn_graph.add_parallel_gateway_to_diagram(self.process_id)

            for event in parallel:
                if event in event_count:
                    event_count[event] += 1
                else:
                    event_count[event] = 1

                self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, parallel_start, event)
                self.flows.append((parallel_start, event))
                self.node_ancestors.setdefault(event, []).append(parallel_start)

                self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, parallel_end)
                self.flows.append((event, parallel_end))
                self.node_successors.setdefault(event, []).append(parallel_end)

        for event in event_count:
            if event_count[event] > 1:
                [gate_anc, _] = self.bpmn_graph.add_exclusive_gateway_to_diagram(self.process_id)
                self.node_ancestors.setdefault(event, []).append(gate_anc)
                [gate_succ, _] = self.bpmn_graph.add_exclusive_gateway_to_diagram(self.process_id)
                self.node_successors.setdefault(event, []).append(gate_succ)

                for i in range(event_count[event]):
                    self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, gate_anc,self.node_ancestors[event][-(i + 2)])
                    self.flows.append((gate_anc,self.node_ancestors[event][-(i + 2)]))
                    self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_successors[event][-(i + 2)], gate_succ)
                    self.flows.append((self.node_successors[event][-(i + 2)], gate_succ))

    def remove_parallel_incomes_outcomes(self):
        parallels = self.footprint.parallels
        for key in self.succession:
            for value in self.succession[key]:
                for parallel in parallels:
                    if value in parallel:
                        for event in parallel:
                            for event2 in parallel:
                                if len(self.node_successors[event]) < len(self.node_successors[event2]) and event in self.succession[key]:
                                    self.succession[key].remove(event)



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
        for event in self.footprint.unique_events:
            used_parallels = []
            if not self.is_in_parallel(event, parallels):
                if event in self.node_ancestors:
                    if len(self.node_ancestors[event]) > 1:
                        for index, id in enumerate(self.node_ancestors[event]):
                            if index + 1 != len(self.node_ancestors[event]):
                               self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_ancestors[event][index+1], id)
                               self.flows.append((self.node_ancestors[event][index+1], id))
                    if not self.is_in_parallel(event, parallels):
                        self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_ancestors[event][0], event)
                        self.flows.append((self.node_ancestors[event][0], event))

                if event in self.node_successors:
                    if len(self.node_successors[event]) > 1:
                        for index, id in enumerate(self.node_successors[event]):
                            if index + 1 != len(self.node_successors[event]):
                               self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, id, self.node_successors[event][index+1])
                               self.flows.append((id, self.node_successors[event][index+1]))

                    if not self.is_in_parallel(event, parallels):
                        self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, self.node_successors[event][0])
                        self.flows.append((event, self.node_successors[event][0]))

            else:
                if len(self.node_successors[event]) > len(self.node_ancestors[event]):
                    self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_successors[event][-2], self.node_successors[event][-1])
                    self.flows.append((self.node_successors[event][-2], self.node_successors[event][-1]))
                elif len(self.node_successors[event]) < len(self.node_ancestors[event]):
                    self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.node_ancestors[event][-1], self.node_ancestors[event][-2])
                    self.flows.append((self.node_ancestors[event][-1], self.node_ancestors[event][-2]))



            if event in self.succession:
                for value in self.succession[event]:
                    if event == value and self.return_dict_value(event, event, self.significance) < self.one_loop_threshhold:
                        continue
                    if not self.is_connected(event, value) and self.return_dict_value(event, value, self.significance) > self.significance_threshhold or [event,value] in self.footprint.find_two_loops() or [value,event] in self.footprint.find_two_loops():
                         if event in self.node_successors and value in self.node_ancestors and not self.is_in_parallel(event, used_parallels):
                             self.add_flow_sucessor_to_ancestor(event, value)
                         elif event in self.node_successors and value not in self.node_ancestors:
                             self.add_flow_successor_to_node(event, value)
                         elif event not in self.node_successors and value in self.node_ancestors:
                             self.add_flow_node_to_ancestor(event,value)
                         elif event not in self.node_successors and value not in self.node_ancestors:
                             self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, value)
                             self.flows.append((event, value))


    def add_flow_sucessor_to_ancestor(self, event, value):
        parallels = self.footprint.parallels
        target = self.node_ancestors[value][-1]
        source = self.node_successors[event][-1]
        for parallel in parallels:
            if event in parallel:
                for event2 in parallel:
                    if len(self.node_successors[event2]) > len(self.node_successors[event]):
                        source = self.node_successors[event2][-1]
            if value in parallel:
                for event2 in parallel:
                    if len(self.node_ancestors[event2]) > len(self.node_ancestors[value]):
                        target = self.node_ancestors[event2][-1]

        self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, source, target)
        self.flows.append((source, target))



    def add_flow_node_to_ancestor(self, event, value):
        parallels = self.footprint.parallels
        target = self.node_ancestors[value][-1]
        for parallel in parallels:
            if event in parallel:
                for event2 in parallel:
                    if len(self.node_ancestors[event2]) > len(self.node_ancestors[value]):
                        target = self.node_ancestors[event2][-1]

        self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event, target)
        self.flows.append((event, target))

    def add_flow_successor_to_node(self, event, value):
        parallels = self.footprint.parallels
        source = self.node_successors[event][-1]
        for parallel in parallels:
            if event in parallel:
                for event2 in parallel:
                    if len(self.node_successors[event2]) > len(self.node_successors[event]):
                        source = self.node_successors[event2][-1]


        self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, source, value)
        self.flows.append((source, value))

    def is_connected(self, source, target):
        availables= []
        availables.append(source)
        if source == target:
            return False
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




