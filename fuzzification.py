def define_line_func(x1, y1, x2, y2):
    def line(x):
        return (y2 - y1) / (x2 - x1) * (x - x2) + y2
    return line


class Point:
    def __init__(self, x, y):
        self.x = x
        self. y = y


class FuzzySet:
    def __init__(self, name, points):
        self.name = name
        self.points = points
        self.line_funcs = []

    def define_line_funcs(self):
        n = len(self.points)
        for i in range(0, n - 1):
            point1 = self.points[i]
            point2 = self.points[i + 1]
            line = define_line_func(point1.x, point1.y, point2.x, point2.y)
            self.line_funcs.append(line)

    def membership(self, x):
        if self.line_funcs is None:
            return -1

        for i in range(0, len(self.points) - 1):
            if self.points[i].x <= x <= self.points[i + 1].x:
                return self.line_funcs[i](x)


class Fuzzifier:
    def __init__(self, name):
        self.name = name
        self.fuzzy_sets = {}

    def add_fuzzy_set(self, name, points):
        new_fuzzy_set = FuzzySet(name, points)
        new_fuzzy_set.define_line_funcs()
        self.fuzzy_sets[new_fuzzy_set.name] = new_fuzzy_set

    def fuzzify(self, x):
        fuzzy_x = {}
        for name, fuzzySet in self.fuzzy_sets.items():
            fuzzy_x[name] = fuzzySet.membership(x)
        return fuzzy_x


# Test
if __name__ == "__main__":
    age_fuzzifier = Fuzzifier("age")
    age_fuzzifier.add_fuzzy_set("age_young", [Point(0, 1), Point(29, 1), Point(38, 0), Point(100, 0)])
    age_fuzzifier.add_fuzzy_set("age_mild", [Point(0, 0), Point(33, 0), Point(38, 1), Point(45, 0), Point(100, 0)])
    age_fuzzifier.add_fuzzy_set("age_old", [Point(0, 0), Point(40, 0), Point(48, 1), Point(58, 0), Point(100, 0)])
    age_fuzzifier.add_fuzzy_set("age_veryold", [Point(0, 0), Point(52, 0), Point(60, 1), Point(100, 1)])
    print(age_fuzzifier.fuzzify(33))
