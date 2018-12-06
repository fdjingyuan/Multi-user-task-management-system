# coding: utf-8

import sys
sys.path.append('../')
from communication.response import Response

class MyException(Exception):
    def __init__(self, error_code, info):
        self.error_code = error_code
        self.info = info

    def toResponse(self):
        return Response(self.error_code, 'ERROR', {'Info': self.info}, '')


class NoSessionInHeader(MyException):
    def __init__(self):
        super(NoSessionInHeader, self).__init__(
            error_code=301,
            info="NO_SESSION_IN_HEADER",
        )

class UserNotExists(MyException):
    def __init__(self):
        super(UserNotExists, self).__init__(
            error_code=302,
            info="USER_NOT_EXISTS",
        )


class DuplicateLogin(MyException):  # Login时的错误
    def __init__(self):
        super(DuplicateLogin, self).__init__(
            error_code=303,
            info="DUPLICATE_LOGIN",
        )

class WrongUserPassword(MyException):
    def __init__(self):
        super(WrongUserPassword, self).__init__(
            error_code=304,
            info="WRONG_USER_PASSWORD",
        )


class SessionNotExists(MyException):
    def __init__(self):
        super(SessionNotExists, self).__init__(
            error_code=305,
            info="SESSION_NOT_EXISTS",
        )


class SessionUserNotMatches(MyException):
    def __init__(self):
        super(SessionUserNotMatches, self).__init__(
            error_code=306,
            info="SESSION_USER_NOT_MATCHES",
        )



class InvalidTaskJson(MyException):
    def __init__(self):
        super(InvalidTaskJson, self).__init__(
            error_code=307,
            info="INVALID_TASK_JSON",
        )


class TaskIDAlreadyExists(MyException):
    def __init__(self):
        super(TaskIDAlreadyExists, self).__init__(
            error_code=308,
            info="TASK_ID_ALREADY_EXISTS",
        )


class TaskTitleRequired(MyException):
    def __init__(self):
        super(TaskTitleRequired, self).__init__(
            error_code=309,
            info="TASK_TITLE_REQUIRED",
        )


class TaskNotExists(MyException):
    def __init__(self):
        super(TaskNotExists, self).__init__(
            error_code=310,
            info="TASK_NOT_EXISTS",
        )


class TaskNotInTheList(MyException):
    def __init__(self):
        super(TaskNotInTheList, self).__init__(
            error_code=311,
            info="TASK_NOT_IN_THE_LIST",
        )


class SameFromAndToList(MyException):
    def __init__(self):
        super(SameFromAndToList, self).__init__(
            error_code=312,
            info="SAME_FROM_AND_TO_LIST",
        )


class InvalidListIndex(MyException):
    def __init__(self):
        super(InvalidListIndex, self).__init__(
            error_code=313,
            info="INVALID_LIST_INDEX",
        )


class UnkownMethod(MyException):
    def __init__(self):
        super(UnkownMethod, self).__init__(
            error_code=314,
            info="UNKNOWN_METHOD",
        )


class ClientConnectionError(MyException):
    def __init__(self):
        super(ClientConnectionError, self).__init__(
            error_code=401,
            info="CLIENT_CONNECTION_ERROR",
        )


class ConnectionClosedUnexpectedly(MyException):
    def __init__(self):
        super(ConnectionClosedUnexpectedly, self).__init__(
            error_code=402,
            info="CONNECTION_CLOSED_UNEXPECTEDLY",
        )


class TooManyConnections(MyException):
    def __init__(self):
        super(TooManyConnections, self).__init__(
            error_code=403,
            info="TOO_MANY_CONNECTIONS",
        )


class InternalError(MyException):
    def __init__(self):
        super(InternalError, self).__init__(
            error_code=500,
            info="INTERNAL_ERROR",
        )
