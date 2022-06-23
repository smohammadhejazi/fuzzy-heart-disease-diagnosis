class Rule:
    def __init__(self, condition, result):
        self.imply_func = None
        self.condition = condition
        self.result = result
        self.initialize()

    def define_imply_func(self, condition_parts, min_max):
        def func(input_params):
            final = None
            if min_max is None:
                return {self.result.split(" IS ")[1]: final}
            else:
                for condition_part in condition_parts:
                    param, p_type = condition_part.split(" IS ")
                    if final is None:
                        final = input_params[param][p_type]
                    else:
                        final = min_max(final, input_params[param][p_type])
                return {self.result.split(" IS ")[1]: final}

        return func

    def initialize(self):
        if "AND" in self.condition:
            condition_parts = self.condition.split("AND")
            condition_parts = [x.strip("() ") for x in condition_parts]
            self.imply_func = self.define_imply_func(condition_parts, min)
        elif "OR" in self.condition:
            condition_parts = self.condition.split("OR")
            condition_parts = [x.strip("() ") for x in condition_parts]
            self.imply_func = self.define_imply_func(condition_parts, max)
        else:
            self.imply_func = self.define_imply_func(self.condition, None)

    def imply(self, inputs):
        if self.imply_func is None:
            return None
        else:
            return self.imply_func(inputs)


class Inference:
    def __init__(self):
        self.rules = []

    def initialize_rules(self):
        with open("rules.fcl") as rules:
            for line in rules:
                main = line.strip(";\n").split(":")[1]
                if_then = main.split("THEN")
                condition = if_then[0][4:].strip()
                result = if_then[1].strip()
                rule = Rule(condition, result)
                self.rules.append(rule)


# Test
if __name__ == "__main__":
    inference = Inference()
    inference.initialize_rules()
    inputs = {
        "age": {
            "young": 0.5,
            "mild": 0.2,
            "old": 0,
            "very_old": 0.1
        },
        "chest_pain": {
            "typical_anginal": 0,
            "atypical_anginal": 1,
            "non_aginal_pain": 0,
            "asymptomatic": 0
        },
    }

    print(inference.rules[0].imply(inputs))

