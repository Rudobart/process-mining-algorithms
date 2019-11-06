
class Footprint:
    def __init__(self, log):
        self.log = log
        self.unique_events = self.find_unique_events()
        self.direct_sucession = self.find_direct_sucession()
        self.start_events = self.find_start_events()
        self.end_events = self.find_end_events()

    def find_unique_events(self):
        unique = []
        for trace in self.log:
            for event in trace:
                if event not in unique:
                    unique.append(event)
        return unique

    def find_direct_sucession(self):
        # ->
        temporal_dependencies = []
        for trace in self.log:
            for index, event in enumerate(trace):
                if index != len(trace) - 1:
                    if (event, trace[index + 1]) not in temporal_dependencies:
                        temporal_dependencies.append((event, trace[index + 1]))
        return temporal_dependencies


    def find_parallels(self):
        # ||
        pararrels = []
        for event in self.unique_events:
            for event2 in self.unique_events:
                if (event,event2) in self.direct_sucession and (event2, event) in self.direct_sucession and (event,event2) not in pararrels and (event2,event) not in pararrels:
                    pararrels.append([event, event2])

        return pararrels

    def max_parallels(self):
        #maximalized parallels
        parallels = self.find_parallels()
        for parallel in parallels:
            for parallel2 in parallels:
                if self.common_event(parallel, parallel2):
                    parallel.extend(parallel2)
                    parallels.remove(parallel2)

        for i in range(len(parallels)):
            parallels[i] = self.unique_list(parallels[i])
        return parallels

    def common_event(self, list1, list2):
        result = False

        for x in list1:
            for y in list2:
                if x == y:
                    result = True
                    return result
        return result

    def unique_list(self, list1):
        unique_list = []
        for x in list1:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list


    def find_independences(self):
        # #
        independences = []
        for event in self.unique_events:
            for event2 in self.unique_events:
                if (event, event2) not in self.direct_sucession and (event2, event) not in self.direct_sucession and (event,event2) not in independences:
                    independences.append((event,event2))
        return independences

    def merge_sucessions(self):
        merged = {}
        i = 0
        used = []
        for dep in self.direct_sucession:
            wanted = dep[0]
            if wanted in used:
                continue
            for it in self.direct_sucession:
                if it[0] == wanted:
                    merged.setdefault(wanted,[])
                    merged[wanted].append(it[1])
            used.append(wanted)
            i += 1
        merged = self.remove_parallels(merged, self.max_parallels())
        return merged

    def remove_parallels(self, dict, parallels):
        for key in dict:
            for parallel in parallels:
                values = dict[key]
                if len(values) > 1:
                    for value in values:
                        if key in parallel and value in parallel:
                            print(value)
                            values.remove(value)
                else:
                    if key in parallel and values in parallel:
                        dict.remove(key)
        return dict

    def find_start_events(self):
        start_events = []
        for trace in self.log:
            if trace[0] not in start_events:
                start_events.append(trace[0])
        return start_events

    def find_end_events(self):
        end_events = []
        for trace in self.log:
            if trace[len(trace)-1] not in end_events:
                end_events.append(trace[len(trace)-1])
        return end_events
