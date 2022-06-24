class Rule:
    def __init__(self, condition, action):
        self._imply_func = None
        self.condition = condition
        self.action = action
        self.initialize()

    def define_imply_func(self, condition_parts, min_max):
        def func(input_params):
            final = None
            # if there is only one condition
            if min_max is None:
                param, p_type = condition_parts.replace(" ", "").replace("\t", "").split("IS")
                if param in input_params:
                    final = input_params[param][p_type]
            # if there are multiple conditions
            else:
                for condition_part in condition_parts:
                    param, p_type = condition_part.replace(" ", "").replace("\t", "").split("IS")
                    if param in input_params:
                        if final is None:
                            final = input_params[param][p_type]
                        else:
                            final = min_max(final, input_params[param][p_type])

            # if nothing fired, final is zero
            if final is None:
                final = 0

            return {self.action.replace(" ", "").replace("\t", "").split("IS")[1]: final}

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
            self.imply_func = self.define_imply_func(self.condition.strip("() "), None)

    def imply(self, inputs):
        if self.imply_func is None:
            return None
        else:
            return self.imply_func(inputs)


class Inference:
    def __init__(self):
        self.rules = []
        self.initialize_rules()

    def initialize_rules(self):
        with open("./rules.fcl") as rules:
            for line in rules:
                if line.strip(";\n") != "":
                    if_then_string = line.strip(";\n").split(":")[1]
                    if_then_parts = if_then_string.split("THEN")
                    condition = if_then_parts[0][4:].strip()
                    action = if_then_parts[1].strip()
                    rule = Rule(condition, action)
                    self.rules.append(rule)

    def imply_all(self, input_params):
        final = {}
        for rule in self.rules:
            result = rule.imply(input_params)
            for key, value in result.items():
                if key not in final:
                    final[key] = value
                else:
                    final[key] = max(final[key], value)
        return final


# Test
if __name__ == "__main__":
    inference = Inference()
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
    # print(inference.rules[11].imply(inputs))
    print(inference.imply_all(inputs))
