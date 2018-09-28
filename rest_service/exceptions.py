from flask_restful import HTTPException


class JeevesServerError(HTTPException):
    def __init__(self, message, status_code=500, payload=None):
        HTTPException.__init__(self, description=message)
        self.code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

    def get_headers(self, environ=None):
        return [('Access-Control-Allow-Origin', ' *')]


class TaskNotFound(JeevesServerError):
    def __init__(self, message, status_code=404, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)


class WorkflowNotFound(JeevesServerError):
    def __init__(self, message, status_code=409, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)


class WorkflowAlreadyExists(JeevesServerError):
    def __init__(self, message, status_code=409, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)


class MissingParameter(JeevesServerError):
    def __init__(self, message, status_code=400, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)


class UnAuthorized(JeevesServerError):
    def __init__(self, message, status_code=401, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)


class InvalidRequestBody(JeevesServerError):
    def __init__(self, message, status_code=400, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)


class UserExists(JeevesServerError):
    def __init__(self, message, status_code=409, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)
