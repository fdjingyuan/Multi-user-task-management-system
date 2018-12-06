# coding: utf-8
from communication.mysocket import Socket, ClientSocket
import json
from communication.request import Request
from misc import errors
import traceback
from misc import utils

class LoginClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = ClientSocket(host, port)
        self.logined = False

    def __parse(self, request):
        if self.sock is None:
            try:
                self.sock = ClientSocket(self.host, self.port)
            except Exception, e:
                return request, e.toResponse()
        self.sock.send(request)
        try:
            response = self.sock.get_response()
        except errors.ConnectionClosedUnexpectedly, e:
            self.sock = None
            return request, e.toResponse()
        if response.code == 200:
            self.logined = True
            self.session_id = response.headers['Session']
        return request, response

    def request_login(self, user, password):
        assert self.logined is False
        verify = utils.get_md5(password)
        request = Request(req='LOGIN', headers={'User': user, 'Verify': verify})
        return self.__parse(request)

    def create_client(self):
        assert self.logined
        return LoginedClient(self.host, self.port, self.sock, self.session_id)

class LoginedClient(object):

    def __init__(self, host, port, sock, session_id):
        self.host = host
        self.port = port
        self.sock = sock
        self.session_id = session_id

    def __parse(self, request):
        if self.sock is None:
            try:
                self.sock = ClientSocket(self.host, self.port)
            except Exception, e:
                return request, e.toResponse()
        self.sock.send(request)
        try:
            response = self.sock.get_response()
        except errors.ConnectionClosedUnexpectedly, e:
            self.sock = None
            return request, e.toResponse()
        return request, response

    def request_list(self):
        request = Request(req='LIST', headers={'Session': self.session_id})
        return self.__parse(request)

    def request_get(self, task_id):
        request = Request(req='GET', headers={'Task-id': task_id, 'Session': self.session_id})
        return self.__parse(request)

    def request_move(self, task_id, from_index, to_index):
        request = Request(req='MOVE', headers={
            'Task-id': task_id,
            'From': from_index,
            'To': to_index,
            'Session': self.session_id
        })
        return self.__parse(request)

    def request_add(self, task_json):
        request = Request(req='ADD', content=json.dumps(task_json), headers={'Session': self.session_id})
        return self.__parse(request)

    def request_update(self, task_json):
        request = Request(req='UPDATE', content=json.dumps(task_json), headers={'Session': self.session_id})
        return self.__parse(request)

    def request_archive(self):
        request = Request(req='ARCHIVE', headers={'Session': self.session_id})
        return self.__parse(request)

    def request_change_theme(self, path):
        request = Request(req='THEME', headers={"Path": path, 'Session': self.session_id})
        return self.__parse(request)

    def request_logout(self):
        request = Request(req='LOGOUT', headers={'Session': self.session_id})
        return self.__parse(request)

    def close(self):
        self.sock.close()

if __name__ == '__main__':
    c = LoginClient('127.0.0.1', 5376)
    print('---------------')
    req, res = c.request_login("ljy", "1")
    print(str(req))
    print(str(res))

    c = c.create_client()
    print('---------------')
    req, res = c.request_logout()
    print(str(req))
    print(str(res))

