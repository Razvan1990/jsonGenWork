import os
import configparser


class TransformerFile:

    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read("config.ini")
        self.filename = self.parser.get("config_helper", "FILENAME")
        self.bracket_left = self.parser.get("config_helper", "BRACKET_LEFT")
        self.bracket_right = self.parser.get("config_helper", "BRACKET_RIGHT")
        self.quote = self.parser.get("config_helper", "QUOTE")
        self.comma = self.parser.get("config_helper", "COMMA")

    def split_key_value(self, word):
        list_words = word.split("=")
        # there will be just 2 words in list , and we need the second parameter, which is the value in our case
        return list_words[1]

    def transform_requirements_list(self, req_string_list):
        string_no_brackets = req_string_list[1:len(req_string_list) - 1]
        list_requirements = string_no_brackets.split(",")
        list_transformed_requirements = []
        for i in range(0, len(list_requirements)):
            if i == len(list_requirements) - 1:
                updated_requirement = self.quote + list_requirements[i] + self.quote
            else:
                updated_requirement = self.quote + list_requirements[i] + self.quote + self.comma
            list_transformed_requirements.append(updated_requirement)
        # transform updated list in a string and add brackets
        final_requirements_strings = self.bracket_left + "".join(list_transformed_requirements) + self.bracket_right
        return final_requirements_strings

    def create_first_list(self):
        global my_file
        current_directory = os.getcwd()
        try:
            list_variables = list()
            my_file = open(file=os.path.join(current_directory, self.filename), mode="r", encoding="utf-8")
            initial_list = my_file.readlines()
            temp_list_full = []
            for idx in range(0, len(initial_list)):
                if idx == len(initial_list) - 1:
                    # last line does not contain '/n, so we need just -1
                    line_ajusted = initial_list[idx][1:len(initial_list[idx]) - 1]
                else:
                    line_ajusted = initial_list[idx][1:len(initial_list[idx]) - 2]
                temp_list_full.append(line_ajusted)
            # split into parameters each element of the list
            for element in temp_list_full:
                list_vars = []
                temp_var_json = element.split(";")
                for i in range(0, len(temp_var_json)):
                    # the last value is the requirements where we need to update with correct form
                    if i == len(temp_var_json) - 1:
                        value_json = self.split_key_value(temp_var_json[i])
                        json_req_var = self.transform_requirements_list(value_json)
                        list_vars.append(json_req_var)
                    else:
                        value_json = self.split_key_value(temp_var_json[i])
                        list_vars.append(value_json)
                list_variables.append(list_vars)
            return list_variables
        except:
            raise FileNotFoundError
        finally:
            my_file.close()
