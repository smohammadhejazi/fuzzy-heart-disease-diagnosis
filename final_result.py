from fuzzification import HeartDiseaseFuzzifier
from inference import Inference


class ProvideResult(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProvideResult, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_final_result(input_dict: dict) -> str:
        input_dict = {'chest_pain': '1', 'cholestrol': '0', 'ecg': '0', 'exercise': '0', 'thallium_scan': '3',
                      'age': '0', 'blood_pressure': '0', 'blood_sugar': '0', 'heart_rate': '0', 'old_peak': '0',
                      'sex': '0'
                      }

        heart_disease_fuzzifier = HeartDiseaseFuzzifier()
        inference = Inference()

        # tidy input dict
        input_dict["cholesterol"] = input_dict.pop("cholestrol")
        input_dict["thallium"] = input_dict.pop("thallium_scan")
        input_dict["maximum_heart_rate"] = input_dict.pop("heart_rate")

        heart_disease_fuzzifier = HeartDiseaseFuzzifier()
        fuzzy_values = {}

        # get fuzzy version of all values
        for param, value in input_dict.items():
            fuzzy_values[param] = heart_disease_fuzzifier.fuzzifiers[param].fuzzify(int(value))

        blood_sugar = {"true": 0, "false": 0}
        if fuzzy_values.pop("blood_sugar")["very_high"] > 120:
            blood_sugar["true"] = 1
            blood_sugar["true"] = 0
        else:
            blood_sugar["true"] = 0
            blood_sugar["true"] = 1
        fuzzy_values["blood_sugar"] = blood_sugar



        print(inference.imply_all(fuzzy_values))


if __name__ == "__main__":
    provideResult = ProvideResult()
    input_dict = {'chest_pain': '1', 'cholestrol': '0', 'ecg': '0', 'exercise': '0', 'thallium_scan': '3', 'age': '0',
                  'blood_pressure': '0', 'blood_sugar': '0', 'heart_rate': '0', 'old_peak': '0', 'sex': '0'}
    provideResult.get_final_result(input_dict)
