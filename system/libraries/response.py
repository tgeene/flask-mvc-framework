# load flask sub-systems
from flask import jsonify


class Response:
    """A tool for handling API responses."""
    _status = {}
    _message = {}

    # -----

    @property
    def status(self) -> dict:
        """Get status dict from string."""
        return {
            'status': self._status
        }

    @status.setter
    def status(self, status: int) -> None:
        """Set status string."""
        self._status = status

    # -----

    @property
    def message(self) -> dict:
        """Get message dict from string."""
        return {
            'message': self._message
        }

    @message.setter
    def message(self, message: str) -> None:
        """Set message string."""
        self._message = message

    # -----

    def respond(self, data: dict = None, status: int = 200, message: str = '') -> str:
        """Generate JSON response."""
        if data is None:
            data = {}

        self.status = status

        if message:
            self.message = message

        return jsonify({**self.status, **self.message, **data})

    def respond_created(self, data: dict, message: str = '') -> str:
        """Create 201 Response."""
        return self.respond(data, 201, message)

    def respond_deleted(self, data: dict, message: str = '') -> str:
        """Create 200 Response."""
        return self.respond(data, 200, message)

    def respond_no_content(self, message: str = 'No Content') -> str:
        """Create 204 Response."""
        return self.respond(status=204, message=message)

    # -----

    def fail(self, message: str = '', status: int = 400, messages=None) -> str:
        """Create Generic Fail Response."""
        if messages is None:
            data = {}
        else:
            data = {
                'messages': messages
            }

        return self.respond(data, status, message)

    def fail_unauthorized(self, message: str = 'Unauthorized') -> str:
        """Create 401 Fail Response."""
        return self.respond(status=401, message=message)

    def fail_forbidden(self, message: str = 'Forbidden') -> str:
        """Create 403 Fail Response."""
        return self.respond(status=403, message=message)

    def fail_not_found(self, message: str = 'Not Found') -> str:
        """Create 404 Fail Response."""
        return self.respond(status=404, message=message)

    def fail_resource_exists(self, message: str = 'Conflict') -> str:
        """Create 409 Fail Response."""
        return self.respond(status=409, message=message)

    def fail_resource_gone(self, message: str = 'Gone') -> str:
        """Create 410 Fail Response."""
        return self.respond(status=410, message=message)


# Assign Class to Variable
response = Response()
