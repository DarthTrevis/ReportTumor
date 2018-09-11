import json

class ReportWriter(object):

    def __init__(self, output_file):
        self.output_file = open("./" + output_file, "w")

    def write_result(self, report_result):

        json_data = json.dumps(report_result.concepts)
        self.output_file.write(json_data + '\n')
        self.output_file.flush()
        #print(report_annotated)