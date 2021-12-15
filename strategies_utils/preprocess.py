#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Preprocessing class of the code.                                            #
# Developed using Python 3.8.                                                 #
#                                                                             #
# Author: Arnaud Tauveron                                                     #
# Linkedin: https://www.linkedin.com/in/arnaud-tauveron/                      #
# Date: 2020-10-14                                                            #
# Version: 1.0.0                                                              #
#                                                                             #
###############################################################################

import pandas as pd
import numpy as np
from typing import Union
import operator as op


class SklPreProcess:
    def __init__(self, X: pd.DataFrame) -> None:
        self.__X__ = X.copy()
        self.X = X.copy()
        self.pipeline_func_ = []

    def execute_function(self, func, args: dict = {}) -> 'SklPreProcess':
        self.pipeline_func_.append({"execute_function": {"func": func}})
        self.X = func(self.X, **args)
        return self

    def add_feature(self, varname: str, init_value) -> 'SklPreProcess':
        self.pipeline_func_.append(
            {"add_feature": {"varname": varname, "init_value": init_value}}
        )
        self.X[varname] = init_value
        return self

    def set_type_var(self, varname: str, type: str) -> 'SklPreProcess':
        self.pipeline_func_.append({"set_type_var": {"varname": varname, "type": type}})
        dict_type = {"str": str, "int": int, "float": float}
        self.X[varname] = self.X[varname].astype(dict_type[type])
        return self

    def insert_value_var(
        self, varname_to_insert: str, query_of_selection: str, value: None
    ) -> 'SklPreProcess':
        self.pipeline_func_.append(
            {
                "insert_value_var": {
                    "varname_to_insert": varname_to_insert,
                    "query_of_selection": query_of_selection,
                    "value": value,
                }
            }
        )
        self.X.loc[self.X.query(query_of_selection).index, varname_to_insert] = value
        return self

    def create_var_relation(self, var1: str, var2: str, operation: str) -> 'SklPreProcess':
        self.pipeline_func_.append(
            {
                "create_var_relation": {
                    "var1": var1,
                    "var2": var2,
                    "operation": operation,
                }
            }
        )
        dict_operands = {"+": op.add, "*": op.mul, "\\": op.truediv}
        self.X[var1 + operation + var2] = dict_operands[operation](
            self.X[var1], self.X[var2]
        )
        return self

    def extract_from_var(
        self, varname: str, varname_extract: str, logic: str
    ) -> 'SklPreProcess':
        self.pipeline_func_.append(
            {
                "extract_from_var": {
                    "varname": varname,
                    "varname_extract": varname_extract,
                    "logic": logic,
                }
            }
        )
        self.X[varname] = self.X[varname_extract].str.extract(logic, expand=False)
        return self

    def fillna_var(self, varname: str, impute_val: float) -> 'SklPreProcess':
        self.pipeline_func_.append(
            {"fillna_var": {"varname": varname, "impute_val": impute_val}}
        )
        self.X[varname] = self.X[varname].fillna(impute_val)
        return self

    def mapping_var(
        self, varname: str, mapping_dict: dict, impute_val: None
    ) -> 'SklPreProcess':
        self.pipeline_func_.append(
            {
                "mapping_var": {
                    "varname": varname,
                    "mapping_dict": mapping_dict,
                    "impute_val": impute_val,
                }
            }
        )
        self.X[varname] = self.X[varname].map(mapping_dict).fillna(impute_val)
        return self

    def categorize_numeric_variables(
        self, varname: str, listcategory: list
    ) -> 'SklPreProcess':
        self.pipeline_func_.append(
            {
                "categorize_numeric_variables": {
                    "varname": varname,
                    "listcategory": listcategory,
                }
            }
        )
        min_ = self.X[varname].min()
        max_ = self.X[varname].max()
        listcategory = list(np.sort(np.unique([min_] + listcategory + [max_])))
        series_cat_ = pd.cut(self.X[varname], bins=listcategory, include_lowest=True)
        listinterval = np.sort(series_cat_.unique())
        dict_cat_ = dict(zip(listinterval, range(len(listinterval))))
        self.X[varname] = series_cat_.replace(dict_cat_)
        return self

    def dropper_col(self, listvar: list, axis=1) -> 'SklPreProcess':
        self.pipeline_func_.append({"dropper_col": {"listvar": listvar, "axis": axis}})
        self.X = self.X.drop(listvar, axis=axis).copy()
        return self

    def dropna_lines(self, listvar: list) -> 'SklPreProcess':
        self.pipeline_func_.append({"dropna_lines": {"listvar": listvar}})
        self.X = self.X.dropna(subset=listvar, axis=0).copy()
        return self

    def set_Xtrain_Ytrain_supervised(self, vartarget: str) -> 'SklPreProcess':
        self.pipeline_func_.append(
            {"dropnset_Xtrain_Ytrain_superviseda_lines": {"vartarget": vartarget}}
        )
        if vartarget in self.X.columnns:
            self.X_train = self.X[[i for i in self.X.columns if vartarget not in i]]
            self.Y_train = self.X[vartarget]
        else:
            self.X_train = None
            self.Y_train = None
        return self

    def compute_dictionnary_func(self, dict_func: dict):
        self.X = self.X.assign(**dict_func)
        return self

    def apply_pipeline(self, module: __module__):
        preprocess_object = SklPreProcess(self.__X__)
        for _dictionnary_temp_ in module.pipeline_func_:
            func_temp_ = list(_dictionnary_temp_.keys())[0]
            args_temp_ = _dictionnary_temp_[func_temp_]
            getattr(preprocess_object, func_temp_)(**args_temp_)
        self.__X__ = preprocess_object.__X__.copy()
        self.X = preprocess_object.X.copy()
        self.pipeline_func_ = preprocess_object.pipeline_func_
        return self
