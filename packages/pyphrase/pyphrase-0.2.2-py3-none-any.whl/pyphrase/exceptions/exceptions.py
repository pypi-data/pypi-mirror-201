class PhraseTMSClientException(Exception):
    pass


class UnableToAuthenticateError(PhraseTMSClientException):
    pass


class NotAuthenticatedError(PhraseTMSClientException):
    pass
