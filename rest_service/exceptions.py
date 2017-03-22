from flask_restful import HTTPException


class JeevesServerError(HTTPException):
    def __init__(self, message, status_code=None, payload=None):
        HTTPException.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload


class TaskNotFound(JeevesServerError):
    def __init__(self, message, status_code=404, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)


class WorkflowNotFound(JeevesServerError):
    def __init__(self, message, status_code=409, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)


class WorkflowAlreadyExists(JeevesServerError):
    def __init__(self, message, status_code=409, payload=None):
        JeevesServerError.__init__(self, message, status_code, payload)
