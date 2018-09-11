#!/usr/bin/env python

class Report:
    def __init__(self, text, tnm_gold):
        self.text = text

        self.tnm_gold = tnm_gold
        self.tnm_classified = None

        self.t_category_gold = None
        self.t_subcategory_gold = None
        self.t_category_classified = None
        self.t_subcategory_classified = None

        self.n_category_gold = None
        self.n_subcategory_gold = None
        self.n_category_classified = None
        self.n_subcategory_classified = None

        self.m_category_gold = None
        self.m_subcategory_gold = None
        self.m_category_classified = None
        self.m_subcategory_classified = None

        self.tumorsize_gold = None
        self.tumorsize_classified = None


        self.concepts = []