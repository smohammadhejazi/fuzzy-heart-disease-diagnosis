from fuzzification import HeartDiseaseFuzzifier
from inference import Inference
from defuzzification import HeartDiseaseDefuzzifier


class ProvideResult(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProvideResult, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def get_final_result(input_dict: dict) -> str:
        heart_disease_fuzzifier = HeartDiseaseFuzzifier()
        inference = Inference()
        heart_disease_defuzzifier = HeartDiseaseDefuzzifier(500)

        # tidy input dict
        input_dict["cholesterol"] = input_dict.pop("cholestrol")
        input_dict["thallium"] = input_dict.pop("thallium_scan")
        input_dict["maximum_heart_rate"] = input_dict.pop("heart_rate")

        fuzzy_values = heart_disease_fuzzifier.fuzzify_all(input_dict)
        print(fuzzy_values)
        fuzzy_outputs = inference.imply_all(fuzzy_values)
        print(fuzzy_outputs)
        output = heart_disease_defuzzifier.deffuzzify(fuzzy_outputs)

        return output


# Test
if __name__ == "__main__":
    provideResult = ProvideResult()
    input_dict = {'chest_pain': '1', 'cholestrol': '0', 'ecg': '0', 'exercise': '0', 'thallium_scan': '3', 'age': '0',
                  'blood_pressure': '0', 'blood_sugar': '0', 'heart_rate': '0', 'old_peak': '0', 'sex': '0'}
    provideResult.get_final_result(input_dict)
