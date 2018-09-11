import unittest
from report_tumor.report_tumor import ReportTumor

report_xlxs = "/Users/sanderputs/Documents/Research/Reports/list_reports_t.xlsx"
output_dir = "./../out"
config_file = "./../config.json"


class TestReportTumor(unittest.TestCase):

    def test_upper(self):
        tnm_classify = ReportTumor(report_xlxs, output_dir, config_file)
        tnm_classify.classify_reports()

if __name__ == '__main__':
    unittest.main()