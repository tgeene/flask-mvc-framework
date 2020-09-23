# load flask sub-systems
from flask import jsonify


# Generate API Response Library
class Response:
    # Initiate Class
    def __init__(self):
        self._status = {}
        self._message = {}

    # -----

    # Return dict from var
    @property
    def status(self):
        return {
            'status': self._status
        }

    # Set var
    @status.setter
    def status(self, status: int):
        self._status = status

    # -----

    # Return dict from var
    @property
    def message(self):
        return {
            'message': self._message
        }

    # Set var
    @message.setter
    def message(self, message: str):
        self._message = message

    # -----

    # Define Root Return Function
    def respond(self, data: dict = None, status: int = 200, message: str = ''):
        if data is None:
            data = {}

        self.status = status

        if message:
            self.message = message

        return jsonify({**self.status, **self.message, **data})

    # Create 201 Response
    def respond_created(self, data: dict, message: str = ''):
        return self.respond(data, 201, message)

    # Create 200 Response
    def respond_deleted(self, data: dict, message: str = ''):
        return self.respond(data, 200, message)

    # Create 204 Response
    def respond_no_content(self, message: str = 'No Content'):
        return self.respond(status=204, message=message)

    # -----

    # Create Generic Fail Response
    def fail(self, message: str = '', status: int = 400, messages=None):
        if messages is None:
            data = {}
        else:
            data = {
                'messages': messages
            }

        return self.respond(data, status, message)

    # Create 401 Fail Response
    def fail_unauthorized(self, message: str = 'Unauthorized'):
        return self.respond(status=401, message=message)

    # Create 403 Fail Response
    def fail_forbidden(self, message: str = 'Forbidden'):
        return self.respond(status=403, message=message)

    # Create 404 Fail Response
    def fail_not_found(self, message: str = 'Not Found'):
        return self.respond(status=404, message=message)

    # Create 409 Fail Response
    def fail_resource_exists(self, message: str = 'Conflict'):
        return self.respond(status=409, message=message)

    # Create 410 Fail Response
    def fail_resource_gone(self, message: str = 'Gone'):
        return self.respond(status=410, message=message)


# Assign Class to Variable
response = Response()
