# load application vars
from application.libraries.database import db

class ExampleModel:
    def __init__(self):
        pass

    def get_users(self):
        records = db.get('users', {}, True)

        return records

example_model = ExampleModel()