#!/usr/bin/env python

import json
import xlrd
from report_tumor.report import Report


# project modules
try:
    from report_tumor import constants
except ImportError:
    from . import constants


class ReportReader(object):

    def __init__(self, config_file):

        with open(config_file, 'r') as f:
            self.config = json.load(f)

    def parse_reports(self, report_xlsx):

        column_name_report = self.config['columns']['report']
        column_name_tnm = self.config['columns']['tnm']

        workbook = xlrd.open_workbook(report_xlsx)
        worksheet = workbook.sheet_by_index(0)

        header_index = 0
        rows = []
        for i, row in enumerate(range(worksheet.nrows)):
            if i == header_index:
                header = self.parse_row(worksheet, i)
            else:
                rows.append(self.parse_row(worksheet, i))

        index_report = header.index(column_name_report)
        index_tnm = header.index(column_name_tnm)

        print(header)
        print('report column={} has index={}'.format(column_name_report, index_report))
        print('tnm column={} has index={}'.format(column_name_tnm, index_tnm))

        reports = []
        for row in rows:
            text = row[index_report]
            tnm_gold = row[index_tnm]
            tnm = self.tnm_replace_x(tnm_gold, self.config['replace-to-x'])

            report = Report(text, tnm)
            reports.append(report)

        return reports

    def parse_row(self, worksheet, row_number):
        r = []
        for j, col in enumerate(range(worksheet.ncols)):
            r.append(worksheet.cell_value(row_number, j))
        return r

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

    def tnm_replace_x(self, label, replace_to_x_list):
        label = label.upper()
        for replace in replace_to_x_list:
            label = label.replace(replace.upper(), 'X')
        return label