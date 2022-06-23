def define_line_func(x1, y1, x2, y2):
    def line(x):
        # if line is singe point
        if x1 == x2 and y1 == y2:
            if x == x1:
                return y1
            else:
                return 0
        # if line is vertical
        elif x1 == x2:
            return None
        else:
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
            # if point is in function domain
            if self.points[i].x <= x <= self.points[i + 1].x:
                return self.line_funcs[i](x)
        # if not in function domain
        else:
            return 0


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


class HeartDiseaseFuzzifier():
    def __init__(self):
        self.fuzzifiers = {}
        self.initialize()

    def initialize(self):
        chest_pain = Fuzzifier("chest_pain")
        chest_pain.add_fuzzy_set("typical_anginal", [Point(1, 1), Point(1, 1)])
        chest_pain.add_fuzzy_set("atypical_anginal", [Point(2, 1), Point(2, 1)])
        chest_pain.add_fuzzy_set("non_aginal_pain", [Point(3, 1), Point(3, 1)])
        chest_pain.add_fuzzy_set("asymptomatic", [Point(4, 1), Point(4, 1)])

        age_fuzzifier = Fuzzifier("age")
        age_fuzzifier.add_fuzzy_set("young", [Point(0, 1), Point(29, 1), Point(38, 0), Point(100, 0)])
        age_fuzzifier.add_fuzzy_set("mild", [Point(0, 0), Point(33, 0), Point(38, 1), Point(45, 0), Point(100, 0)])
        age_fuzzifier.add_fuzzy_set("old", [Point(0, 0), Point(40, 0), Point(48, 1), Point(58, 0), Point(100, 0)])
        age_fuzzifier.add_fuzzy_set("very_old", [Point(0, 0), Point(52, 0), Point(60, 1), Point(100, 1)])

        blood_pressure = Fuzzifier("blood_pressure")
        blood_pressure.add_fuzzy_set("low", [Point(100, 1), Point(111, 1), Point(134, 0), Point(300, 0)])
        blood_pressure.add_fuzzy_set("medium", [Point(100, 0), Point(127, 0), Point(139, 1), Point(153, 0), Point(300, 0)])
        blood_pressure.add_fuzzy_set("high", [Point(100, 0), Point(142, 0), Point(157, 1), Point(172, 0), Point(300, 0)])
        blood_pressure.add_fuzzy_set("very_high", [Point(100, 0), Point(154, 0), Point(171, 1), Point(300, 1)])

        blood_sugar = Fuzzifier("blood_sugar")
        blood_sugar.add_fuzzy_set("very_high", [Point(60, 0), Point(105, 0), Point(120, 1), Point(160, 1)])

        cholesterol = Fuzzifier("cholesterol")
        cholesterol.add_fuzzy_set("low", [Point(100, 1), Point(151, 1), Point(199, 0), Point(400, 0)])
        cholesterol.add_fuzzy_set("medium", [Point(100, 0), Point(188, 0), Point(215, 1), Point(250, 0), Point(400, 0)])
        cholesterol.add_fuzzy_set("high", [Point(100, 0), Point(217, 0), Point(263, 1), Point(307, 0), Point(400, 0)])
        cholesterol.add_fuzzy_set("ver_high", [Point(100, 0), Point(281, 0), Point(347, 1), Point(400, 1)])

        heart_rate = Fuzzifier("heart_rate")
        heart_rate.add_fuzzy_set("low", [Point(0, 1), Point(100, 1), Point(191, 0), Point(500, 0)])
        heart_rate.add_fuzzy_set("medium", [Point(0, 0), Point(111, 0), Point(152, 1), Point(194, 0), Point(500, 0)])
        heart_rate.add_fuzzy_set("high", [Point(0, 0), Point(152, 0), Point(210, 1), Point(500, 1)])

        ecg = Fuzzifier("ecg")
        ecg.add_fuzzy_set("normal", [Point(-0.5, 1), Point(0, 1), Point(0.4, 0), Point(2.5, 0)])
        ecg.add_fuzzy_set("abnormal", [Point(-0.5, 0), Point(0.2, 0), Point(1, 1), Point(1.8, 0), Point(2.5, 0)])
        ecg.add_fuzzy_set("hypertrophy", [Point(-0.5, 0), Point(1.4, 0), Point(1.9, 1), Point(2.5, 1)])

        old_peak = Fuzzifier("old_peak")
        old_peak.add_fuzzy_set("low", [Point(0, 1), Point(1, 1), Point(2, 0), Point(6, 0)])
        old_peak.add_fuzzy_set("risk", [Point(0, 0), Point(1.5, 0), Point(2.8, 1), Point(4.2, 0), Point(6, 0)])
        old_peak.add_fuzzy_set("terrible", [Point(0, 0), Point(2.5, 0), Point(4.1, 1), Point(6, 1)])

        self.fuzzifiers["chest_pain"] = chest_pain
        self.fuzzifiers["age"] = age_fuzzifier
        self.fuzzifiers["blood_pressure"] = blood_pressure
        self.fuzzifiers["blood_sugar"] = blood_sugar
        self.fuzzifiers["cholesterol"] = cholesterol
        self.fuzzifiers["heart_rate"] = heart_rate
        self.fuzzifiers["ecg"] = ecg
        self.fuzzifiers["old_peak"] = old_peak


# Test
if __name__ == "__main__":
    main_fuzzifier = HeartDiseaseFuzzifier()

    print("chest_pain: " + str(main_fuzzifier.fuzzifiers["chest_pain"].fuzzify(1)))
    print("ecg: " + str(main_fuzzifier.fuzzifiers["ecg"].fuzzify(0.3)))

