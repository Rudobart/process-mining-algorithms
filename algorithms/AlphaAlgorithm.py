from config import *



class AlphaAlgorithm():

    def find_unique_events(self,log):
        unique = []
        for trace in log:
            for event in trace:
                if event not in unique:
                    unique.append(event)
        return unique

    def find_temporal_dependencies(self, log):
        # ->
        temporal_dependencies = []
        for trace in log:
            for index, event in enumerate(trace):
                if index != len(trace) - 1:
                    if (event, trace[index + 1]) not in temporal_dependencies:
                        temporal_dependencies.append((event, trace[index + 1]))
        return temporal_dependencies


    def find_temporal_independencies(self, unique, temporal_dependencies):
        # ||
        temporal_independencies = []
        for event in unique:
            for event2 in unique:
                if (event,event2) in temporal_dependencies and (event2, event) in temporal_dependencies and (event,event2) not in temporal_independencies and (event2,event) not in temporal_independencies:
                    temporal_independencies.append((event,event2))
        return temporal_independencies

    def find_independences(self, unique, temporal_dependencies):
        # #
        independences = []
        for event in unique:
            for event2 in unique:
                if (event, event2) not in temporal_dependencies and (event2, event) not in temporal_dependencies and (event,event2) not in independences:
                    independences.append((event,event2))
        return independences

    def find_start_events(self, log):
        start_events = []
        for trace in log:
            if trace[0] not in start_events:
                start_events.append(trace[0])
        return start_events

    def find_end_events(self, log):
        end_events = []
        for trace in log:
            if trace[len(trace)-1] not in end_events:
                end_events.append(trace[len(trace)-1])
        return end_events

    def merge_dependencies(self, temporal_dependencies):
        merged = {}
        i = 0
        used = []
        for dep in temporal_dependencies:
            wanted = dep[0]
            if wanted in used:
                continue
            for it in temporal_dependencies:
                if it[0] == wanted:
                    merged.setdefault(wanted,[])
                    merged[wanted].append(it[1])
            used.append(wanted)
            i += 1
        return merged

alpha = AlphaAlgorithm()
print(log_list)
print(alpha.find_temporal_dependencies(log_list))
print(alpha.find_unique_events(log_list))
print(alpha.find_temporal_independencies(alpha.find_unique_events(log_list),alpha.find_temporal_dependencies(log_list)))
print(alpha.find_independences(alpha.find_unique_events(log_list),alpha.find_temporal_dependencies(log_list)))
print(alpha.find_start_events(log_list))
print(alpha.find_end_events(log_list))
print(alpha.merge_dependencies(alpha.find_temporal_dependencies(log_list)))
