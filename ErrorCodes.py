# -*- coding: utf-8 -*-

"""Contains the error codes and the exception thrown by the program
when an error is detected"""

SUCCESS = 0
GENERIC_FAILURE = 1
INVALID_SQUARE_SELECTION = 2


ERROR_MESSAGES = {
    SUCCESS: 'success',
    GENERIC_FAILURE: 'generic failure',
    INVALID_SQUARE_SELECTION: 'Invalid input! Square must belong in chess board!',

}


class ErrorException(Exception):

    """ ErrorException is raised when an error is detected"""

    def __init__(self, error_code, message=None):
        super(ErrorException, self).__init__()
        self.error_code = error_code
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        if self.error_code in ERROR_MESSAGES:
            return ERROR_MESSAGES[self.error_code]
        return 'unknown error (%d)' % self.error_code

    def exit(self):
        exception = SystemExit()
        exception.code = self.error_code
        exception.message = str(self)
        raise exception

    def is_error(self):
        return self.error_code != 0
