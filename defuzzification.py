from fuzzification import define_line_func, Point, FuzzySet
import numpy as np


class Defuzzifier:
    def __init__(self, name, number_of_points):
        self.name = name
        self.number_of_points = number_of_points
        self.fuzzy_sets = {}

    def add_fuzzy_set(self, name, points):
        new_fuzzy_set = FuzzySet(name, points)
        new_fuzzy_set.define_line_funcs()
        self.fuzzy_sets[new_fuzzy_set.name] = new_fuzzy_set

    def defuzzify(self, fuzzy_outputs):
        fuzzy_sets_xy = {}
        x_points = np.linspace(0, 5, self.number_of_points)

        for name, fuzzySet in self.fuzzy_sets.items():
            y_output = fuzzy_outputs[name]
            print(y_output)
            y_points = []
            for x in x_points:
                y_points.append(min(fuzzySet.membership(x), y_output))
            fuzzy_sets_xy[name] = y_points


        numerator = 0
        denominator = 0
        for x in range(self.number_of_points):
            tmp = None
            for name, y_points in fuzzy_sets_xy.items():
                if tmp is None:
                    tmp = y_points[x]
                else:
                    tmp = max(y_points[x], tmp)
            numerator += tmp * x_points[x]
            denominator += tmp

        crisp_x = numerator / denominator

        final_output = {}
        for name, fuzzySet in self.fuzzy_sets.items():
            y = fuzzySet.membership(crisp_x)
            if y != 0:
                final_output[name] = y

        return final_output


class HeartDiseaseDefuzzifier:
    def __init__(self, number_of_points):
        self.defuzzifier = None
        self.number_of_points = number_of_points
        self.initialize()

    def deffuzzify(self, fuzzy_outputs):
        return self.defuzzifier.defuzzify(fuzzy_outputs)

    def initialize(self):
        # Crisp inputs

        health = Defuzzifier("health", self.number_of_points)
        health.add_fuzzy_set("healthy", [Point(0, 1), Point(0.25, 1), Point(1, 0), Point(5, 0)])
        health.add_fuzzy_set("sick_1", [Point(0, 0), Point(1, 1), Point(2, 0), Point(5, 0)])
        health.add_fuzzy_set("sick_2", [Point(0, 0), Point(1, 0), Point(2, 1), Point(3, 0), Point(5, 0)])
        health.add_fuzzy_set("sick_3", [Point(0, 0), Point(2, 0), Point(3, 1), Point(4, 0), Point(5, 0)])
        health.add_fuzzy_set("sick_4", [Point(0, 0), Point(3, 0), Point(4, 1), Point(5, 0), Point(5, 0)])

        self.defuzzifier = health
