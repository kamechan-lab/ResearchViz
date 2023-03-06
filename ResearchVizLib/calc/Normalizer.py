from typing import List

import pandas
from pandas import DataFrame


class Normalizer:
    data :List[DataFrame]
    normalized_data :List[DataFrame] = []
    max_values_list :list
    mul_list = []
    max_val : float

    def __init__(self, data):
        self.data = data
        self.createMaxValuesList()
        self.findBiggest()
        self.createMulList()
        self.normalize()

    def createMaxValuesList(self):
        list = []
        for d in self.data:
            l = []
            for i, series in enumerate(d.iteritems()):
                if(not i == 0):
                    l.append(series[1].max())
            list.append(l)
        self.max_values_list = list
        return list

    def findBiggest(self):
        l = []
        for list in self.max_values_list:
            l.append(max(list))
        self.max_val = max(l)
        return self.max_val

    def createMulList(self):
        for l in self.max_values_list:
            self.mul_list.append(list(map(lambda input: input / self.max_val, l)))
        return self.mul_list

    def normalize(self):
        for i, d in enumerate(self.data):
            normalized_df = 0
            for j, series in enumerate(d.iteritems()):
                if(j == 0):
                    normalized_df = d[d.columns[0]]
                else:
                    normalized_df = pandas.concat([normalized_df, (d.iloc[:, j] / self.mul_list[i][j - 1])], axis=1)
            self.normalized_data.append(normalized_df)
        return self.normalized_data



d = pandas.read_csv("C:\\Users\\genko\\Documents\\Lab\\FDTD_data\\sio0_sio1_sio3_sio5_sio7_sio10_sio15_sio20_sio30\\extinction_sio0_sio1_sio3_sio5_sio7_sio10_sio15_sio20_sio30.txt", sep="\t" )
norm = Normalizer([d])
norm.normalized_data[0].to_csv("C:\\Users\\genko\\Documents\\Lab\\FDTD_data\\sio0_sio1_sio3_sio5_sio7_sio10_sio15_sio20_sio30\\extinction_sio0_sio1_sio3_sio5_sio7_sio10_sio15_sio20_sio30_normalized.txt", sep="\t", index=False)

