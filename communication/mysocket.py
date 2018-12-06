# coding: utf-8
import sys
sys.path.append('../')

import socket, sys
from misc import errors
import json
from .response import Response
from .request import Request


class Socket(object):
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def recv_fixed_length(self, length):
        data = ''
        while len(data) < length:
            more = self.sock.recv(length - len(data))
            if not more:
                raise errors.ConnectionClosedUnexpectedly
            data += more
        return data

    def send(self, request_or_response):
        self.sock.sendall(str(request_or_response))

    def get_response(self):
        info = self.recv_fixed_length(24 + 2)  # 2是第一行最后的\r\n
        code = int(info[0:3])
        res = info[4:14].strip()
        length = int(info[14:24].strip())
        content_and_headers = self.recv_fixed_length(length)
        content_and_headers = content_and_headers.split('\r\n')
        headers = {}
        for line_index, line in enumerate(content_and_headers):
            if line == '':
                break
            else:
                key = line.split(':')[0]
                value = line.split(':')[1]
                headers[key] = value
        content = '\r\n'.join(content_and_headers[line_index + 1:])
        return Response(code=code, res=res, headers=headers, content=content)

    def get_request(self):
        info = self.recv_fixed_length(20 + 2)  # 2是第一行最后的\r\n
        req = info[0:10].strip()
        length = int(info[10:20].strip())
        content_and_headers = self.recv_fixed_length(length)
        content_and_headers = content_and_headers.split('\r\n')
        headers = {}
        for line_index, line in enumerate(content_and_headers):
            if line == '':
                break
            else:
                key = line.split(':')[0]
                value = line.split(':')[1]
                headers[key] = value
        content = '\r\n'.join(content_and_headers[line_index + 1:])

        return Request(req=req, headers=headers, content=content)

    def close(self):
        self.sock.close()

class ServerSocket(Socket):
    def __init__(self, host, port):
        super(ServerSocket, self).__init__()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(10)

class ClientSocket(Socket):
    def __init__(self, host, port):
        super(ClientSocket, self).__init__()
        try:
            self.sock.connect((host, port))
        except Exception:
            raise errors.ClientConnectionError







