# -*- coding: utf-8 -*-
# author: 华测-长风老师
# file name：excel_to.py

import xlrd


class Excel:
    def __init__(self, excel_name):
        self.excel_name = excel_name
        self.sheet_name = None
        self.excel = None
        self.sheet = None

    def get_excel(self):
        self.excel = xlrd.open_workbook(filename=self.excel_name)
        return self.excel

    def get_sheet_by_name(self):
        excel = xlrd.open_workbook(filename=self.excel_name)
        self.sheet = excel.sheet_by_name(self.sheet_name)
        return self.sheet

    def get_key_value_list_to_json(self, start=1, end=None):
        if end is None:
            self.get_sheet_by_name()
            l = []
            row_nums = self.sheet.nrows
            col_nums = self.sheet.ncols
            names = self.sheet.row_values(0)
            for row in range(start, row_nums):
                app = {}
                for col in range(0, col_nums):
                    app[names[col]] = self.sheet.cell_value(row, col)
                l.append(app)
            return l

    def get_key_value_list_to_tuple(self, start=1, end=None):
        if end is None:
            self.get_sheet_by_name()
            l = []
            row_nums = self.sheet.nrows
            col_nums = self.sheet.ncols
            names = self.sheet.row_values(0)
            for row in range(start, row_nums):
                app = {}
                for col in range(0, col_nums):
                    app[names[col]] = self.sheet.cell_value(row, col)
                l.append(tuple(app.values()))
            return tuple(l)

    def get_key_value_list_to_list(self, start=1, end=None):
        if end is None:
            self.get_sheet_by_name()
            l = []
            row_nums = self.sheet.nrows
            col_nums = self.sheet.ncols
            names = self.sheet.row_values(0)
            for row in range(start, row_nums):
                app = {}
                for col in range(0, col_nums):
                    app[names[col]] = self.sheet.cell_value(row, col)
                l.append(list(app.values()))
            return l


if __name__ == '__main__':
    e = Excel("fileName")
    e.sheet_name = "sheetName"
    data_ = e.get_key_value_list_to_list(start=2)
    print(data_)
