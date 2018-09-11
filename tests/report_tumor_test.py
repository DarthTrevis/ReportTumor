import unittest
from report_tumor.report_reader import ReportReader
from report_tumor.report_writer import ReportWriter

from report_tumor.report_tumor import ReportTumor
from report_tumor.report import Report


report_xlxs = "/Users/sanderputs/Documents/Research/Reports/list_reports_t.xlsx"
output_file = "./../result.txt"
config_file = "./../config.json"


class TestReportTumor(unittest.TestCase):

    def test_upper(self):
        report_reader = ReportReader(config_file)
        report_writer = ReportWriter(output_file)

        report_tumor = ReportTumor()

        reports = report_reader.parse_reports(report_xlxs);

        total_reports = len(reports)
        for idx, report in enumerate(reports):

            print('{}'.format('report ' + str(idx+1) + '/' + str(total_reports)))
            report_tumor.classify_report(report)
            report_writer.write_result(report)


if __name__ == '__main__':
    unittest.main()