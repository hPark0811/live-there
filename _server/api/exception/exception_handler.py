from flask import jsonify

# referenced to: https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
class GenericException(Exception):
    def __init__(self, message='Internal server error', status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

class BadRequest(GenericException):
    def __init__(self, message='Bad request exception', status_code=400, payload=None):
        GenericException.__init__(self, message, status_code, payload)
