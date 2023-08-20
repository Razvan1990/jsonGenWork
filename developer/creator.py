import os
import configparser
from developer.transformer import TransformerFile
import developer.constants


class FileCreator:

    def __init__(self):
        self.transformer = TransformerFile()
        self.parser = configparser.ConfigParser()
        self.parser.read("config.ini")
        self.testcases = self.parser.get("config_helper", "CASES")
        self.description = self.parser.get("config_helper", "DESCRIPTION")
        self.model = self.parser.get("config_helper", "MODEL")
        self.name = self.parser.get("config_helper", "NAME")
        self.parameter = self.parser.get("config_helper", "PARAM")
        self.prepfile = self.parser.get("config_helper", "PREPARATION_FILE")
        self.reference = self.parser.get("config_helper", "REFERENCE")
        self.requirements = self.parser.get("config_helper", "REQUIREMENTS")
        self.scaling = self.parser.get("config_helper", "SCALING")
        self.vector_file = self.parser.get("config_helper", "TEST_VECTOR_FILE")
        self.tolerance_file = self.parser.get("config_helper", "TOLERANCE")
        self.bracket_left = self.parser.get("config_helper", "BRACKET_LEFT")
        self.bracket_right = self.parser.get("config_helper", "BRACKET_RIGHT")
        self.quote = self.parser.get("config_helper", "QUOTE")
        self.comma = self.parser.get("config_helper", "COMMA")
        self.colon = self.parser.get("config_helper", "COLON")
        self.model_name = input("Introduce the model name ")

    def create_coverage_string(self):
        mcdc_applicable = input("Is MCDC applicable for the model? Type Y or N ").upper()
        while mcdc_applicable != "N" and mcdc_applicable != "Y":
            print("Not a correct option. Type a valid option")
            mcdc_applicable = input("Is MCDC applicable for the model? Type Y or N ").upper()
        # make logic of mcdc now
        if mcdc_applicable == "Y":
            mcdc_value = 1.0
        else:
            mcdc_value = -1.0

        coverage_string = """
    "CoverageSetting": "MCDC",
    "CoverageThresholds": [
        {
            "CyclomaticComplexity": 99999,
            "Decision": 1.0,
            "Execution": 1.0,
            "MCDC": """ + str(mcdc_value) + """
        }
    ],"""
        return coverage_string

    def create_json_test(self):
        coverage_settings_string = self.create_coverage_string()
        has_argumentation = input("Is there an argumentation file for the model? Type Y or N ").upper()
        while has_argumentation != "N" and has_argumentation != "Y":
            print("Not a correct option. Type a valid option")
            has_argumentation = input("Is there an argumenration file for the model? Type Y or N ").upper()
        # check for argumentation
        if has_argumentation == "Y":
            argumentation_file = developer.constants.ARGUMENTATION_FILE + self.colon + developer.constants.ARGUMENTATION_NAME + self.model_name + ".json" + self.quote
        else:
            argumentation_file = ""

        # start testcase generation
        TEST_STRING = ""
        list_tests = self.transformer.create_first_list()
        for i in range(0, len(list_tests)):
            description, parameters, requirements = list_tests[i][0], list_tests[i][1], list_tests[i][2]
            if i == len(list_tests) - 1:
                if i < 10:
                    TEST_STRING += "\n\t\t\t{" + "\n\t\t\t\t" + self.description + ":" + self.quote + description + self.quote + self.comma + "\n\t\t\t\t" + self.model + ":" + """ "", """ + "\n\t\t\t\t" + self.name + ":" + \
                                   """ "m_""" + self.model_name + "_TC0" + str(
                        i + 1) + """", """ + "\n\t\t\t\t" + self.parameter + ":" + developer.constants.PARAM_FILE + parameters + """ .m", """ + "\n\t\t\t\t" + \
                                   self.prepfile + ":" + developer.constants.SCRIPT_FILE + "0" + str(
                        i + 1) + """.m", """ + "\n\t\t\t\t" + self.reference + ":" + """ "", """ + "\n\t\t\t\t" + self.requirements + ":" + requirements + self.comma + "\n\t\t\t\t" + \
                                   self.scaling + ":" + """ "",""" + "\n\t\t\t\t" + self.vector_file + ":" + """ "",""" + "\n\t\t\t\t" + self.tolerance_file + ":" + """ "" """ + "\n\t\t\t}"
                else:
                    TEST_STRING += "\n\t\t\t{" + "\n\t\t\t\t" + self.description + ":" + self.quote + description + self.quote + self.comma + "\n\t\t\t\t" + self.model + ":" + """ "", """ + "\n\t\t\t\t" + self.name + ":" + \
                                   """ "m_""" + self.model_name + "_TC" + str(
                        i + 1) + """", """ + "\n\t\t\t\t" + self.parameter + ":" + developer.constants.PARAM_FILE + parameters + """ .m", """ + "\n\t\t\t\t" + \
                                   self.prepfile + ":" + developer.constants.SCRIPT_FILE + str(
                        i + 1) + """.m", """ + "\n\t\t\t\t" + self.reference + ":" + """ "", """ + "\n\t\t\t\t" + self.requirements + ":" + requirements + self.comma + "\n\t\t\t\t" + \
                                   self.scaling + ":" + """ "",""" + "\n\t\t\t\t" + self.vector_file + ":" + """ "",""" + "\n\t\t\t\t" + self.tolerance_file + ":" + """ "" """ + "\n\t\t\t}"
            else:
                if i < 10:
                    TEST_STRING += "\n\t\t\t{" + "\n\t\t\t\t" + self.description + ":" + self.quote + description + self.quote + self.comma + "\n\t\t\t\t" + self.model + ":" + """ "", """ + "\n\t\t\t\t" + self.name + ":" + \
                                   """ "m_""" + self.model_name + "_TC0" + str(
                        i + 1) + """", """ + "\n\t\t\t\t" + self.parameter + ":" + developer.constants.PARAM_FILE + parameters + """ .m", """ + "\n\t\t\t\t" + \
                                   self.prepfile + ":" + developer.constants.SCRIPT_FILE + "0" + str(
                        i + 1) + """.m", """ + "\n\t\t\t\t" + self.reference + ":" + """ "", """ + "\n\t\t\t\t" + self.requirements + ":" + requirements + self.comma + "\n\t\t\t\t" + \
                                   self.scaling + ":" + """ "",""" + "\n\t\t\t\t" + self.vector_file + ":" + """ "",""" + "\n\t\t\t\t" + self.tolerance_file + ":" + """ "" """ + "\n\t\t\t},"
                else:
                    TEST_STRING += "\n\t\t\t{" + "\n\t\t\t\t" + self.description + ":" + self.quote + description + self.quote + self.comma + "\n\t\t\t\t" + self.model + ":" + """ "", """ + "\n\t\t\t\t" + self.name + ":" + \
                                   """ "m_""" + self.model_name + "_TC" + str(
                        i + 1) + """", """ + "\n\t\t\t\t" + self.parameter + ":" + developer.constants.PARAM_FILE + parameters + """ .m", """ + "\n\t\t\t\t" + \
                                   self.prepfile + ":" + developer.constants.SCRIPT_FILE + str(
                        i + 1) + """.m", """ + "\n\t\t\t\t" + self.reference + ":" + """ "", """ + "\n\t\t\t\t" + self.requirements + ":" + requirements + self.comma + "\n\t\t\t\t" + \
                                   self.scaling + ":" + """ "",""" + "\n\t\t\t\t" + self.vector_file + ":" + """ "",""" + "\n\t\t\t\t" + self.tolerance_file + ":" + """ "" """ + "\n\t\t\t},"
        # creation of final string
        if argumentation_file != "":
            TEST_JSON = "{" + coverage_settings_string + "\n\t" + self.name + ":" + developer.constants.TEST_FILE_NAME + self.model_name + """" """ + self.comma + "\n\t" + argumentation_file + self.comma + "\n\t" + self.testcases + ":[" + TEST_STRING + "\n\t]" + "\n}"
        else:
            TEST_JSON = "{" + coverage_settings_string + "\n\t" + self.name + ":" + developer.constants.TEST_FILE_NAME + self.model_name + """" """ + self.comma + "\n\t" + self.testcases + ":[" + TEST_STRING + "\n\t]" + "\n}"
        return TEST_JSON

    def create_file(self):
        json_test = self.create_json_test()
        os.chdir("generation")
        filename = developer.constants.FILE_GENERATOR_NAME + self.model_name +".json"
        with open(file=filename, mode="w", encoding="utf-8") as test_file:
            test_file.write(json_test)
        print("The {} has been generated in the following location {}.".format(filename, os.getcwd()))
        os.startfile(filename)

