class Footprint:
    def __init__(self, log, algorithm_name):
        self.algorithm_name = algorithm_name
        self.log = log
        self.unique_events = self.find_unique_events()
        self.direct_sucession = self.find_direct_sucession()
        self.start_events = self.find_start_events()
        self.end_events = self.find_end_events()
        self.succession = self.merge_sucessions()
        self.parallels = self.find_parallels()
        self.node_incomes = self.count_node_incomes(self.succession, self.parallels)
        self.node_outcomes = self.count_node_outcomes(self.succession, self.parallels)

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
        parallels = []
        two_loops = self.find_two_loops()
        for event in self.unique_events:
            for event2 in self.unique_events:
                if (event, event2) in self.direct_sucession and (event2, event) in self.direct_sucession and [event, event2] not in parallels and [event2, event] not in parallels and event != event2:
                    parallels.append([event, event2])

        if self.algorithm_name == "alpha":
            return parallels

        for two_loop in two_loops:
            for parallel in parallels:
                for event in parallel:
                    for event2 in parallel:
                        if event in two_loop and event2 in two_loop:
                            if [event, event2] in parallels:
                                parallels.remove([event, event2])
                            if [event2, event] in parallels:
                                parallels.remove([event2, event])
        return parallels

    def max_parallels(self):
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
                    return (result, x)
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

    def find_one_loops(self):
        one_loops = []
        for trace in self.log:
            for index, event in enumerate(trace):
                if index+1 != len(trace):
                    if event == trace[index+1]:
                        one_loops.append(event)
        return one_loops


    def find_two_loops(self):
        two_loops = []
        for trace in self.log:
            for index, event in enumerate(trace):
                if index+2 < len(trace):
                    if event == trace[index+2]:
                        two_loops.append([event, trace[index+1]])

        return two_loops


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
        self.remove_parallels(self.find_parallels(), merged)
        return merged

    def remove_parallels(self, parallels, dict):
        for parallel in parallels:
            for event in parallel:
                for event2 in parallel:
                    if event != event2:
                        dict[event].remove(event2)



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

    def count_node_incomes(self, succession, parallels):
        incomes = {}
        for key in succession:
            for value in succession[key]:
                if value not in incomes.keys():
                    incomes[value] = 1
                else:
                    incomes[value] += 1
                for parallel in parallels:
                    if key in parallel and value in incomes:
                        incomes[value] -= (len(parallel)-1)


        return incomes





    def count_node_outcomes(self, succession, parallels):
        outcomes = {}
        for key in succession:
            if key in succession[key]:
                outcomes[key] = len(succession[key]) - 1
            else:
                outcomes[key] = len(succession[key])
            for parallel in parallels:
                for value in succession[key]:
                    if value in parallel:
                        outcomes[key] -= (len(parallel) - 1)
                    break

        return outcomes


