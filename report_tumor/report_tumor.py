#!/usr/bin/env python

import json
import xlrd

from report_tumor.annotate_umls import AnnotateUMLS


def get_overwrites(header, overwrite_map):
    overwrites = {}
    for k, v in overwrite_map.items():
        try:
            index = header.index(k)
            overwrites[index] = v
        except ValueError as err:
            print(header)
            print("ValueError not in header: {0}".format(err))
    return overwrites


class ReportTumor(object):

    # project modules
    try:
        from report_tumor import constants
    except ImportError:
        from . import constants

    report_csv = ""
    output_dir = ""
    rows = []
    index_report = -1
    index_tnm = -1

    def __init__(self, report_xlsx, output_dir, config_file):
        self.output_dir = output_dir

        with open(config_file, 'r') as f:
            self.config = json.load(f)

        self.output_file = open("./" + "classify.txt", "w")

        self.annotate_umls = AnnotateUMLS()
        self.parse_reports(report_xlsx, self.config)


    def parse_reports(self, report_xlsx, config):
        column_name_report = config['columns']['report']
        column_name_tnm = config['columns']['tnm']

        workbook = xlrd.open_workbook(report_xlsx)
        worksheet = workbook.sheet_by_index(0)

        header_index = 0
        for i, row in enumerate(range(worksheet.nrows)):
            if i == header_index:
                header = self.parse_row(worksheet, i)
            else:
                self.rows.append(self.parse_row(worksheet, i))

        self.index_report = header.index(column_name_report)
        self.index_tnm = header.index(column_name_tnm)

        print(header)
        print('report column={} has index={}'.format(column_name_report, self.index_report))
        print('tnm column={} has index={}'.format(column_name_tnm, self.index_tnm))

    def parse_row(self, worksheet, row_number):
        r = []
        for j, col in enumerate(range(worksheet.ncols)):
            r.append(worksheet.cell_value(row_number, j))
        return r

    def classify_reports(self):

        totalReports = len(self.rows)

        for idx, row in enumerate(self.rows):
            print('report ' + str(idx+1) + '/' + str(totalReports))

            tnm = row[self.index_tnm]
            report = row[self.index_report]
            tnm = self.tnm_replace_x(tnm, self.config['replace-to-x'])
            t = self.tnm_get_t(tnm)
            n = self.tnm_get_n(tnm)
            m = self.tnm_get_m(tnm)

            print('{}'.format(tnm))
            print('{}'.format(t))
            print('{}'.format(n))
            print('{}'.format(m))

            report_annotated = self.annotate_report(report)
            json_data = json.dumps(report_annotated)

            self.output_file.write(json_data + '\n')
            self.output_file.flush()
            #print(report_annotated)

    def tnm_replace_x(self, label, replace_to_x_list):
        label = label.upper()
        for replace in replace_to_x_list:
            label = label.replace(replace.upper(), 'X')
        return label

    @staticmethod
    def tnm_get_t(label):
        label = label.split("N")
        return label[0]

    @staticmethod
    def tnm_get_n(label):
        if not label:
            return label
        return "N"+label.split("N")[1].split("M")[0]

    @staticmethod
    def tnm_get_m(label):
        if not label:
            return label
        return "M"+label.split("M")[1]

    def annotate_report(self, report):
        report = self.annotate_umls.annotate(report)
        return report

