from fuzzification import HeartDiseaseFuzzifier

class ProvideResult(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProvideResult, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_final_result(input_dict: dict) -> str:
        main_fuzzifier = HeartDiseaseFuzzifier()
        fuzzy_values = {}

        # get fuzzy version of all values
        for param, value in input_dict.items():
            fuzzy_values[param] = main_fuzzifier.fuzzifiers[param].fuzzify(value)
