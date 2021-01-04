# load py systems
import re
import validators
from typing import Union

# load flask sub-systems
from flask import request

# load system libraries
from system.libraries.database import db


# Generate Form Validation Library
class FormValidation:
    """A tool for handling web form validation."""
    _fields = {}
    _inputs = {}
    _errors = []

    # -----

    def add_field(self, field_name: str, field_label: str, field_rules: str) -> None:
        """Add Field to Validation List."""
        field = {
            'name': field_name,
            'label': field_label,
            'rules': field_rules
        }
        self._fields[field_name] = field

    def validate(self) -> dict:
        """Handle Validation of Form."""
        content = {}
        if request.is_json:
            content = request.get_json()

        for field in self._fields:
            value = ""
            if request.method == "POST":
                if content:
                    value = content[self._fields[field]['name']]
                else:
                    value = request.form.get(self._fields[field]['name'])
            elif request.method == "GET":
                value = request.values.get(self._fields[field]['name'])

            self._inputs[self._fields[field]['name']] = value

            rules = self._fields[field]['rules'].split("|")

            process = True
            for rule in rules:
                if process:
                    rule_parts = list(filter(None, re.split('([^\[]+)', rule)))

                    method_name = "_" + rule_parts[0]
                    if len(rule_parts) == 1:
                        method = getattr(self, method_name, (lambda x, y: 'Invalid'))
                        results = method(self._fields[field]['name'], value)
                    else:
                        method = getattr(self, method_name, (lambda x, y, z: 'Invalid'))
                        results = method(self._fields[field]['name'], value, rule_parts[2].rstrip("]"))

                    if not results:
                        process = False
                    elif results == 'Invalid':
                        self._errors.append(f"{field['label']} config is invalid.")
                        process = False

        result = {
            'errors': self._errors,
            'inputs': self._inputs
        }
        return result

    # -----

    def _required(self, field: str, value: Union[float, int, str]) -> bool:
        """Validate if Value has a value."""
        if value is None or not value:
            self._errors.append(f"{self._fields[field]['label']} is a required field.")
            return False

        return True

    def _matches(self, field: str, value: Union[float, int, str], match: str) -> bool:
        """Validate if Value matches other Field."""
        if match not in self._fields:
            self._errors.append(f"{self._fields[field]['label']} match field not submitted for validation.")
            return False

        if request.method == "POST":
            match_value = request.form.get(match)
        else:
            match_value = request.values.get(match)

        if value != match_value:
            self._errors.append(f"{self._fields[field]['label']} does not match {self._fields[match]['label']}.")
            return False

        return True

    def _differs(self, field: str, value: Union[float, int, str], match: str) -> bool:
        """Validate if Value different than other Field."""
        if match not in self._fields:
            self._errors.append(f"{self._fields[field]['label']} match field not submitted for validation.")
            return False

        if request.method == "POST":
            match_value = request.form.get(match)
        else:
            match_value = request.values.get(match)

        if value == match_value:
            self._errors.append(f"{self._fields[field]['label']} cannot match {self._fields[match]['label']}.")
            return False

        return True

    def _regex_match(self, field: str, value: Union[float, int, str], regex: str) -> bool:
        """Validate if Value matches regex."""
        regex_parts = list(filter(None, re.split('([\/]+)', regex)))

        flags = 0
        if 1 in regex_parts:
            flag_options = {
                'a': re.A,
                'i': re.I,
                'L': re.L,
                'm': re.M,
                's': re.S,
                'u': re.U,
                'x': re.X
            }
            for flag in flag_options:
                if flag in regex_parts[1]:
                    if flags != 0:
                        flags |= flag_options[flag]
                    else:
                        flags = flag_options[flag]

        if not re.match(regex_parts[0], value, flags):
            self._errors.append(f"{self._fields[field]['label']} does not meet the correct pattern.")
            return False

        return True

    def _min_length(self, field: str, value: Union[float, int, str], length: str) -> bool:
        """Validate if Value is greater than or equal to num of characters."""
        if len(str(value)) < int(length):
            self._errors.append(f"{self._fields[field]['label']} must be at least {length} characters long.")
            return False

        return True

    def _max_length(self, field: str, value: Union[float, int, str], length: str) -> bool:
        """Validate if Value is less than or equal to num of characters."""
        if len(str(value)) > int(length):
            self._errors.append(f"{self._fields[field]['label']} cannot be longer than {length} characters long.")
            return False

        return True

    def _exact_length(self, field: str, value: Union[float, int, str], length: str) -> bool:
        """Validate if Value is exact number of characters."""
        if len(str(value)) == int(length):
            self._errors.append(f"{self._fields[field]['label']} must be exactly {length} characters long.")
            return False

        return True

    def _greater_than(self, field: str, value: Union[float, int, str], num: str) -> bool:
        """Validate if Value > Num"""
        if float(value) < float(num):
            self._errors.append(f"{self._fields[field]['label']} must be more than {num}.")
            return False

        return True

    def _greater_than_equal_to(self, field: str, value: Union[float, int, str], num: str) -> bool:
        """Validate if Value >= Num"""
        if float(value) <= float(num):
            self._errors.append(f"{self._fields[field]['label']} must be at least {num}.")
            return False

        return True

    def _less_than(self, field: str, value: Union[float, int, str], num: str) -> bool:
        """Validate if Value < Num."""
        if float(value) > float(num):
            self._errors.append(f"{self._fields[field]['label']} must be less than {num}.")
            return False

        return True

    def _less_than_equal_to(self, field: str, value: Union[float, int, str], num: str) -> bool:
        """Validate if Value <= Num."""
        if float(value) >= float(num):
            self._errors.append(f"{self._fields[field]['label']} cannot be bigger than {num}.")
            return False

        return True

    def _in_list(self, field: str, value: Union[float, int, str], options: str) -> bool:
        """Validate if Value is in List."""
        options = options.split(',')

        if value not in options:
            self._errors.append(f"{self._fields[field]['label']} is not an accepted value.")
            return False

        return True

    def _in_db(self, field: str, value: Union[float, int, str], db_select: str) -> bool:
        """Validate if Value is in Database."""
        db_parts = db_select.split('.')

        where = {
            db_parts[1]: value
        }
        if not db.get_count(db_parts[0], where):
            self._errors.append(f"{self._fields[field]['label']} is not an accepted value.")
            return False

        return True

    def _alpha(self, field: str, value: Union[float, int, str]) -> bool:
        """Validate if Value is only Letters."""
        if not re.match('^[a-zA-Z]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters.")
            return False

    def _alpha_dash(self, field: str, value: Union[float, int, str]) -> bool:
        """Validate if Value is only Letters, Dashes, and Underscores."""
        if not re.match('^[a-zA-Z\-_]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters, dashes, and underscores.")
            return False

        return True

    def _alpha_numeric(self, field: str, value: Union[float, int, str]) -> bool:
        """Validate if Value is only Letters and Numbers."""
        if not re.match('^[a-zA-Z0-9]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters and numbers.")
            return False

    def _alpha_numeric_dash(self, field: str, value: Union[float, int, str]) -> bool:
        """Validate if Value is only Letters, Numbers, Dashes, and Underscores."""
        if not re.match('^[a-zA-Z0-9\-_]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters, numbers, dashes, and underscores.")
            return False

    def _alpha_space(self, field: str, value: Union[float, int, str]) -> bool:
        """Validate if Value is only Letters and Spaces."""
        if not re.match('^[a-zA-Z ]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters and spaces.")
            return False

        return True

    def _alpha_numeric_space(self, field: str, value: Union[float, int, str]) -> bool:
        """Validate if Value is only Letters, Numbers, and Spaces."""
        if not re.match('^[a-zA-Z0-9 ]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters, numbers, and spaces.")
            return False

        return True

    def _numeric(self, field: str, value: Union[float, int, str]) -> bool:
        """Validate if Value is a Number."""
        if not re.match('^[0-9.]+$', value):
            self._errors.append(f"{self._fields[field]['label']} must be a number.")
            return False

        return True

    def _valid_email(self, field: str, value: str) -> bool:
        """Validate if String is Email."""
        if validators.email(value) is not True:
            self._errors.append(f"{self._fields[field]['label']} must be a valid email.")
            return False

        return True

    def _valid_url(self, field: str, value: str) -> bool:
        """Validate if String is URL."""
        if validators.url(value) is not True:
            self._errors.append(f"{self._fields[field]['label']} must be a valid URL.")
            return False

        return True


# Assign Class to Variable
form_validation = FormValidation()
