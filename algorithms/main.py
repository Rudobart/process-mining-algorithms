# import unittest
#
# import bpmn_python.bpmn_diagram_layouter as layouter
# import bpmn_python.bpmn_diagram_visualizer as visualizer
# import bpmn_python.bpmn_diagram_rep as diagram
# from config import *
# from algorithms.Alpha import *
#
#
#
#
#
#
# bpmn_graph = diagram.BpmnDiagramGraph()
# bpmn_graph.create_new_diagram_graph(diagram_name="diagram1")
# process_id = bpmn_graph.add_process_to_diagram()
# [start_id, _] = bpmn_graph.add_start_event_to_diagram(process_id, start_event_name="start_event",
#                                                       start_event_definition="timer")
# [task1_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task1")
# bpmn_graph.add_sequence_flow_to_diagram(process_id, start_id, task1_id, "start_to_one")
#
# [exclusive_gate_fork_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
#                                                                           gateway_name="exclusive_gate_fork")
# [task1_ex_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task1_ex")
# [task2_ex_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task2_ex")
# [exclusive_gate_join_id, _] = bpmn_graph.add_exclusive_gateway_to_diagram(process_id,
#                                                                           gateway_name="exclusive_gate_join")
#
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_id, exclusive_gate_fork_id, "one_to_ex_fork")
# bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, task1_ex_id, "ex_fork_to_ex_one")
# bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_fork_id, task2_ex_id, "ex_fork_to_ex_two")
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task1_ex_id, exclusive_gate_join_id, "ex_one_to_ex_join")
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_ex_id, exclusive_gate_join_id, "ex_two_to_ex_join")
#
# [task2_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task2")
# [end_id, _] = bpmn_graph.add_end_event_to_diagram(process_id, end_event_name="end_event",
#                                                   end_event_definition="message")
# bpmn_graph.add_sequence_flow_to_diagram(process_id, exclusive_gate_join_id, task2_id, "ex_join_to_two")
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task2_id, end_id, "two_to_end")
#
# [task3_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task3")
# [task4_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task4")
# [task5_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task5")
# [task6_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task6")
# [task7_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task7")
# [task8_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task8")
# [task9_id, _] = bpmn_graph.add_task_to_diagram(process_id, task_name="task8")
#
#
#
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task9_id, task3_id)
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task9_id, task4_id)
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task9_id, task5_id)
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task6_id, task9_id)
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task7_id, task9_id)
# bpmn_graph.add_sequence_flow_to_diagram(process_id, task8_id, task9_id)
# print(bpmn_graph.get_nodes())
#
#
# #bpmn_graph.add_sequence_flow_to_diagram(process_id, task4_id, task3_id)
#
#
#
#
#
#
#
#
#
#
# layouter.generate_layout(bpmn_graph)
# print(bpmn_graph.get_nodes())
# alpha = Alpha(log_list)
# alpha.build_bpmn()
#
# # Uncomment line below to get a simple view of created diagram
# #visualizer.visualize_diagram(bpmn_graph)
# bpmn_graph.export_xml_file(output_directory, "simple_diagram.bpmn")


def is_connected( source, target):
    availables = []
    availables.append(source)
    for ava in availables:
        for tuple in [(1,2),(1,3),(3,4),(5,6),(4,5)]:
            if tuple[0] == ava and tuple[1] not in availables:
                availables.append(tuple[1])

    if target in availables:
        return True
    return False

print(is_connected(3,6))