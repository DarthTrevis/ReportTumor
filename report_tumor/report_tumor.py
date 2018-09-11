#!/usr/bin/env python

from report_tumor.annotate_umls import AnnotateUMLS

class ReportTumor(object):


    def __init__(self):
        self.annotate_umls = AnnotateUMLS()

    def classify_report(self, report):

        tnm = report.tnm_gold

        report.t_category_gold = self.tnm_get_t(tnm)
        report.t_category_gold = self.tnm_get_n(tnm)
        report.m_category_gold= self.tnm_get_m(tnm)

        report_annotated = self.annotate_report(report)
        return report_annotated



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
        report.concepts = self.annotate_umls.annotate(report.text)
        return report

