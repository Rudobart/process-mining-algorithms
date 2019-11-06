from config import *
import bpmn_python.bpmn_diagram_layouter as layouter
import bpmn_python.bpmn_diagram_visualizer as visualizer
import bpmn_python.bpmn_diagram_rep as diagram
from algorithms.utils import Footprint as footprint

class Alpha:
    def __init__(self, log):
        self.log = log
        self.footprint = footprint(self.log)
        self.sucession = self.footprint.merge_sucessions()
        self.bpmn_graph = diagram.BpmnDiagramGraph()
        self.bpmn_graph.create_new_diagram_graph(diagram_name="alpha_alogrithm_bpmn")
        self.process_id = self.bpmn_graph.add_process_to_diagram()
        self.nodes_id = {}



    def build_bpmn(self):
        for start_event in self.footprint.start_events:
            [start_id, _] = self.bpmn_graph.add_start_event_to_diagram(self.process_id,start_event_definition="timer")
            [start_event_id, _] = self.bpmn_graph.add_task_to_diagram(self.process_id, task_name=start_event)
            self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, start_id, start_event_id)
            self.nodes_id[start_event] = start_event_id
            self.add_node(start_event, start_event_id, [])



        for end_event in self.footprint.end_events:
            if end_event in self.nodes_id.keys():
                [end_id, _] = self.bpmn_graph.add_end_event_to_diagram(self.process_id, end_event_definition="message")
                self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, self.nodes_id[end_event], end_id)




        #print(self.bpmn_graph.get_nodes())
        #print(len(self.bpmn_graph.get_flows()))
        layouter.generate_layout(self.bpmn_graph)
        # Uncomment line below to get a simple view of created diagram
        #visualizer.visualize_diagram(bpmn_graph)
        self.bpmn_graph.export_xml_file(output_directory, "alpha_algorithm.bpmn")




    def add_node(self, event, event_id, used):
        for key in self.sucession.keys():
            if key == event and key not in used:
                if len(self.sucession[key]) > 1:
                    for value in self.sucession[key]:
                        if value in self.nodes_id.keys():
                            task_id = self.nodes_id[value]
                        else:
                            [task_id, _] = self.bpmn_graph.add_task_to_diagram(self.process_id, task_name=value)
                            self.nodes_id[value] = task_id

                        self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event_id, task_id)
                        used.append(key)
                        self.add_node(value, task_id, used)


                elif len(self.sucession[key])==1:
                     event = self.sucession[key][0]
                     if event in self.nodes_id.keys():
                         task_id = self.nodes_id[event]
                     else:
                         [task_id, _] = self.bpmn_graph.add_task_to_diagram(self.process_id, task_name=event)
                         self.nodes_id[event] = task_id

                     self.bpmn_graph.add_sequence_flow_to_diagram(self.process_id, event_id, task_id)


                     used.append(key)
                     self.add_node(event, task_id, used)


alpha = Alpha(log_list)
print(alpha.sucession)
alpha.build_bpmn()