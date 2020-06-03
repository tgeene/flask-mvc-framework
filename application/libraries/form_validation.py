# load py systems
import re
import validators

# load flask sub-systems
from flask import request

# load system libraries
from application.libraries.database import *

# Generate Form Validation Library
class FormValidation:
    _fields = {}
    _inputs = {}
    _errors = []

    def __init__(self):
        pass

    def add_field(self, field_name, field_label, field_rules):
        field = {
            'name': field_name,
            'label': field_label,
            'rules': field_rules
        }
        self._fields[field_name] = field

    def validate(self):
        for field in self._fields:
            if request.method == "POST":
                value = request.form.get(self._fields[field]['name'])
            else:
                value = request.values.get(self._fields[field]['name'])

            self._inputs[self._fields[field]['name']] = value

            rules = self._fields[field]['rules'].split("|")

            process = True
            for rule in rules:
                if process:
                    rule_parts = list(filter(None, re.split('([^\[]+)', rule)))

                    method_name = "_" + rule_parts[0]
                    if 1 not in rule_parts:
                        method = getattr(self, method_name, (lambda x, y: 'Invalid'))
                        results = method(self._fields[field]['name'], value)
                    else:
                        method = getattr(self, method_name, (lambda x, y, z: 'Invalid'))
                        results = method(self._fields[field]['name'], value, rule_parts[1].rstrip("]"))

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

    def _required(self, field, value):
        if value is None or not value:
            self._errors.append(f"{self._fields[field]['label']} is a required field.")
            return False

        return True

    def _matches(self, field, value, match):
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

    def _differs(self, field, value, match):
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

    def _regex_match(self, field, value, regex):
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

    def _min_length(self, field, value, length):
        value = str(value)

        if len(value) < length:
            self._errors.append(f"{self._fields[field]['label']} must be at least {length} characters long.")
            return False

        return True

    def _max_length(self, field, value, length):
        value = str(value)

        if len(value) > length:
            self._errors.append(f"{self._fields[field]['label']} cannot be longer than {length} characters long.")
            return False

        return True

    def _exact_length(self, field, value, length):
        value = str(value)

        if len(value) == length:
            self._errors.append(f"{self._fields[field]['label']} must be exactly {length} characters long.")
            return False

        return True

    def _greater_than(self, field, value, num):
        if 'int' in type(num):
            value = int(value)
        else:
            value = float(value)

        if value < num:
            self._errors.append(f"{self._fields[field]['label']} must be more than {num}.")
            return False

        return True

    def _greater_than_equal_to(self, field, value, num):
        if 'int' in type(num):
            value = int(value)
        else:
            value = float(value)

        if value <= num:
            self._errors.append(f"{self._fields[field]['label']} must be at least {num}.")
            return False

        return True

    def _less_than(self, field, value, num):
        if 'int' in type(num):
            value = int(value)
        else:
            value = float(value)

        if value > num:
            self._errors.append(f"{self._fields[field]['label']} must be less than {num}.")
            return False

        return True

    def _less_than_equal_to(self, field, value, num):
        if 'int' in type(num):
            value = int(value)
        else:
            value = float(value)

        if value >= num:
            self._errors.append(f"{self._fields[field]['label']} cannot be bigger than {num}.")
            return False

        return True

    def _in_list(self, field, value, options):
        options = options.split(',')

        if value not in options:
            self._errors.append(f"{self._fields[field]['label']} is not an accepted value.")
            return False

        return True

    def _in_db(self, field, value, db_select):
        db_parts = db_select.split('.')

        where = {
            db_parts[1]: value
        }
        if not db.get_count(db_parts[0], where):
            self._errors.append(f"{self._fields[field]['label']} is not an accepted value.")
            return False

        return True

    def _alpha(self, field, value):
        if not re.match('^[a-zA-Z]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters.")
            return False

    def _alpha_dash(self, field, value):
        if not re.match('^[a-zA-Z\-_]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters, dashes, and underscores.")
            return False

        return True

    def _alpha_numeric(self, field, value):
        if not re.match('^[a-zA-Z0-9]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters and numbers.")
            return False

    def _alpha_numeric_dash(self, field, value):
        if not re.match('^[a-zA-Z0-9\-_]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters, numbers, dashes, and underscores.")
            return False

    def _alpha_space(self, field, value):
        if not re.match('^[a-zA-Z ]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters and spaces.")
            return False

        return True

    def _alpha_numeric_space(self, field, value):
        if not re.match('^[a-zA-Z0-9 ]+$', value):
            self._errors.append(f"{self._fields[field]['label']} may only have letters, numbers, and spaces.")
            return False

        return True

    def _numeric(self, field, value):
        if not re.match('^[0-9.]+$', value):
            self._errors.append(f"{self._fields[field]['label']} must be a number.")
            return False

        return True

    def _valid_email(self, field, value):
        if validators.email(value) is not True:
            self._errors.append(f"{self._fields[field]['label']} must be a valid email.")
            return False

        return True

    def _valid_url(self, field, value):
        if validators.url(value) is not True:
            self._errors.append(f"{self._fields[field]['label']} must be a valid URL.")
            return False

        return True

form_validation = FormValidation()