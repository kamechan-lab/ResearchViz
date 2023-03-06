from pandas import DataFrame, Series


class MathUtil:

    def obtainRiemannSumSections(self, x: Series, y: Series) ->list:
        rec_areas = []
        for i in range(len(x)):
            if not i == len(x) - 1:
                dx = x[i + 1] - x[i]
                rec_areas.append(dx * y[i])
            else:
                rec_areas.append(0)
        return rec_areas

    def absRiemannSum(self, x: Series, y: Series):
        abs_rec_areas = []
        for i in self.obtainRiemannSumSections(x, y):
            abs_rec_areas.append(abs(i))
        return abs_rec_areas

    def calcExtinction(self, main: Series, base: Series, rfl = False):
        pass



def isFloat(str: str):
    try:
        float(str)
        return True
    except(ValueError):
        return False