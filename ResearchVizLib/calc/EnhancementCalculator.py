import glob
import pandas
from pandas import DataFrame, Series
from ResearchUtils.BaseFileManager import BaseFileManager
from ResearchUtils.MathUtil import MathUtil


class FdtdEnhAnalyzer:
    math_util = MathUtil()
    main: DataFrame
    base: DataFrame

    rfl_enh = 0
    xmt_enh = 0
    tot_enh = 0

    def __init__(self, main: DataFrame, base: DataFrame, trimmed=False):
        self.setData(main, base, trimmed)
        self.computeRflEnh()
        self.computeXmtEnh()
        self.computeTotEnh()

    def setData(self, main: DataFrame, base: DataFrame, trimmed=False):
        if(trimmed):
            self.main = main
            self.base = base
        else:
            self.main = main.iloc[:, [0, 5, 9]]
            self.base = base.iloc[:, [0, 1, 9]]
        self.main.columns = ["wl", "xmt", "rfl"]
        self.base.columns = ["wl", "xmt", "rfl"]



    def computeRflEnh(self):
        main_rfl_area = sum(self.math_util.absRiemannSum(self.main["wl"], self.main["rfl"]))
        base_rfl_area = sum(self.math_util.absRiemannSum(self.base["wl"], self.base["rfl"]))
        self.rfl_enh = main_rfl_area / base_rfl_area
        return self.rfl_enh

    def computeXmtEnh(self):
        main_xmt_area = sum(self.math_util.absRiemannSum(self.main["wl"], self.main["xmt"]))
        base_xmt_area = sum(self.math_util.absRiemannSum(self.base["wl"], self.base["xmt"]))
        self.xmt_enh = main_xmt_area / base_xmt_area
        return self.xmt_enh

    def computeTotEnh(self):
        main_rfl_area = sum(self.math_util.absRiemannSum(self.main["wl"], self.main["rfl"]))
        main_xmt_area = sum(self.math_util.absRiemannSum(self.main["wl"], self.main["xmt"]))
        base_rfl_area = sum(self.math_util.absRiemannSum(self.base["wl"], self.base["rfl"]))
        base_xmt_area = sum(self.math_util.absRiemannSum(self.base["wl"], self.base["xmt"]))
        self.tot_enh = (main_rfl_area + main_xmt_area)/(base_xmt_area + base_rfl_area)
        return self.tot_enh


    def exportAsTuple(self):
        return (self.xmt_enh, self.rfl_enh, self.tot_enh)


