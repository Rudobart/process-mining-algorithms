from opyenxes.classification.XEventAttributeClassifier import XEventAttributeClassifier
from opyenxes.data_in.XUniversalParser import XUniversalParser

file_path = "/home/bartlomiej/process-mining/process-mining-algorithms/event_logs/bigger-example.xes"
output_directory = "./output/"



with open(file_path) as log_file:
    # Parse the log
    log = XUniversalParser().parse(log_file)[0]

# Generate the classifier
classifier = XEventAttributeClassifier("concept:name", ["concept:name"])

# Convert log object in array with only the Activity attribute of the event
log_list = list(map(lambda trace: list(map(classifier.get_class_identity, trace)), log))

