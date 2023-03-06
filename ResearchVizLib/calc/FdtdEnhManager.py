import glob
import os

from pandas import DataFrame
import pandas
from SignAnalyzer import SignPath
from BaseFileManager import BaseFileManager
from EnhancementCalculator import FdtdEnhAnalyzer

class FdtdEnhUtil:

    dir_file: str
    bfm = BaseFileManager()
    enh_data = DataFrame(index=["xmt", "rfl", "tot"])

    def __init__(self, dir_file: str):
        self.dir_file = dir_file
        self.__acquireEnhData()
        self.exportAsTSV()

    def setDirFile(self, dir_file: str):
        self.dir_file = dir_file
        self._getEnhData().drop(self._getEnhData().columns)
        self.__acquireEnhData()

    def _getEnhData(self):
        return self.enh_data

    def __acquireEnhData(self):
        dir_files = glob.glob(self.dir_file + "\\*")
        base_files = self.bfm.extractBaseFiles(dir_files)
        for bf in base_files:
            main_file = self.bfm.findPair(bf, dir_files)
            d = SignPath(main_file).obtainSignVal("d")
            enhance = FdtdEnhAnalyzer(pandas.read_csv(main_file), pandas.read_csv(bf)).exportAsTuple()
            self.enh_data[d] = enhance
        self._getEnhData().sort_index(axis="columns", inplace=True)

    def exportAsTSV(self):
        self._getEnhData().to_csv(os.path.join(self.dir_file, "enhancement.txt"), sep="\t", mode="w")


enh_manager = FdtdEnhUtil("C:\\Users\\genko\\Documents\\Lab\\FDTD_data\\SiO2 0 nm revised")
#a = SignPath('C:\\Users\\genko\\Documents\\python_test\\d90_base.txt').obtainSignVal("d")
#print(a)