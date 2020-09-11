# load flask sub-systems
from flask import jsonify

# Generate API Response Library
class Response:
    def __init__(self):
        self._status = {}
        self._message = {}

    # -----

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: int):
        self._status = {
            'status': status
        }

    # -----

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message: str):
        self._message = {
            'message': message
        }

    # -----

    def respond(self, data: dict = None, status: int = 200, message: str = ''):
        if data is None:
            data = {}

        self.status = status

        if message:
            self.message = message

        return jsonify({**self.status, **self.message, **data})

    def respond_created(self, data: dict, message: str = ''):
        return self.respond(data, 201, message)

    def respond_deleted(self, data: dict, message: str = ''):
        return self.respond(data, 200, message)

    def respond_no_content(self, message: str = 'No Content'):
        return self.respond(status=204, message=message)

    # -----

    def fail(self, message: str = '', status: int = 400, messages=None):
        if messages is None:
            data = {}
        else:
            data = {
                'messages': messages
            }

        return self.respond(data, status, message)

    def fail_unauthorized(self, message: str = 'Unauthorized'):
        return self.respond(status=401, message=message)

    def fail_forbidden(self, message: str = 'Forbidden'):
        return self.respond(status=403, message=message)

    def fail_not_found(self, message: str = 'Not Found'):
        return self.respond(status=404, message=message)

    def fail_resource_exists(self, message: str = 'Conflict'):
        return self.respond(status=409, message=message)

    def fail_resource_gone(self, message: str = 'Gone'):
        return self.respond(status=410, message=message)


response = Response()