# load application vars
from system.libraries.database import db


class ExampleModel:
    def __init__(self):
        pass

    def get_users(self):
        records = db.get('users')

        return records


example_model = ExampleModel()
