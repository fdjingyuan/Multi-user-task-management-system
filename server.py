# coding: utf-8
from __future__ import print_function
from communication.mysocket import Socket, ServerSocket
import codecs
import json
from communication.response import Response
import traceback
from misc import errors
import thread
import uuid

class Server(object):

    '''
    sessions:
    {
        "session_id":
        {
            "username": username
            "data_list": data_list        
        }
    }


    users:
    {
        user_name: {
            "verify": verify_string
        }
    }
    '''
    sessions = {}
    users = {}

    def __init__(self, host, port, user_file="data/user/user", data_path='data/'):
        self.sock = ServerSocket(host, port)
        self.data_path = data_path
        self.user_file = user_file
        self.load_user()

    def load_user(self):
        with open(self.user_file, 'r') as f:
            self.users = json.load(f, encoding='utf-8')

    def save_user(self):
        with open(self.user_file, 'w') as f:
            json.dump(self.users, f, encoding='utf-8')

    def load_data(self, session_id):
        username = self.sessions[session_id]['username']
        with open(self.data_path + username, 'r') as f:
            self.sessions[session_id]["data_list"] = json.load(f, encoding='utf-8')

    def write_data(self, session_id):
        username = self.sessions[session_id]['username']
        with open(self.data_path + 'bak/' + username, 'w') as f:
            json.dump(self.sessions[session_id]["data_list"], f, encoding='utf-8')
        with open(self.data_path + username, 'w') as f:
            json.dump(self.sessions[session_id]["data_list"], f, encoding='utf-8')

    def assert_request_session(self, request, username):
        if 'Session' not in request.headers:
            raise errors.NoSessionInHeader
        session_id = request.headers['Session']
        if str(session_id) not in self.sessions:
            raise errors.SessionNotExists
        if username != self.sessions[session_id]['username']:
            raise errors.SessionUserNotMatches

    def run_session(self, socket):
        session_id = str(uuid.uuid1())
        self.lock.acquire()  # 全局的修改操作最好加个锁
        self.sessions[session_id] = {}
        self.lock.release()
        is_login = False
        print('Session {} starts.'.format(session_id))
        try:
            while True:
                request = socket.get_request()
                try:
                    if request.req == 'LOGIN' and is_login is False:
                        is_login = self.respond_login(socket, request, session_id)
                        if is_login:
                            print(str(request))
                            session_username = request.headers['User']
                            self.lock.acquire()
                            self.sessions[session_id]['username'] = session_username
                            self.lock.release()
                            self.load_data(session_id)
                    elif request.req == 'LOGIN' and is_login is True:
                        socket.send(errors.DuplicateLogin().toResponse())
                    elif request.req == 'LOGOUT' and is_login is True:
                        # logout时检查下session是否正确
                        try:
                            self.assert_request_session(request, session_username)
                        except errors.MyException, e:
                            socket.send(e.toResponse())
                            continue
                        if self.respond_logout(socket, request, session_id):
                            print(str(request))
                            self.write_data(session_id)
                            break
                    elif request.req == 'LOGOUT' and is_login is False:
                        socket.send(errors.NoSessionInHeader().toResponse())
                    else:
                        if is_login is False:
                            socket.send(errors.NoSessionInHeader().toResponse())
                        else:
                            try:
                                self.assert_request_session(request, session_username)
                            except errors.MyException, e:
                                socket.send(e.toResponse())
                                continue
                            if request.req == 'LIST':
                                self.respond_list(socket, request, session_id)
                            elif request.req == 'GET':
                                self.respond_get(socket, request, session_id)
                            elif request.req == 'MOVE':
                                self.respond_move(socket, request, session_id)
                            elif request.req == 'ADD':
                                self.respond_add(socket, request, session_id)
                            elif request.req == 'UPDATE':
                                self.respond_update(socket, request, session_id)
                            elif request.req == 'ARCHIVE':
                                self.respond_archive(socket, request, session_id)
                            elif request.req == 'THEME':
                                self.respond_theme(socket, request, session_id)
                            else:
                                socket.send(errors.UnkownMethod().toResponse())
                            self.write_data(session_id)
                except Exception:  # 处理一个请求时的内部错误。内部错误不应影响后续请求的处理
                    traceback.print_exc()
                    socket.send(errors.InternalError().toResponse())
        except Exception:  # 可能的网络断线
            traceback.print_exc()
        if is_login:
            self.write_data(session_id)
        print('Session {} ends.'.format(session_id))
        del self.sessions[session_id]

    def run(self):
        try:
            self.lock = thread.allocate()
            raw_sock = self.sock.sock
            print('Listening at', raw_sock.getsockname())
            while True:
                socket, sockname = raw_sock.accept()  # 可以多次调用
                socket = Socket(socket)  # 该socket用来回答request
                thread.start_new_thread(self.run_session, (socket,))
        except Exception:  # 服务器级别的错误
            traceback.print_exc()
            self.sock.close()

    def check_task_json(self, task_json):
        if 'id' not in task_json:
            return False
        elif 'title' not in task_json:
            return False
        return True

    def respond_login(self, socket, request, session_id):
        username = request.headers['User']
        verify = request.headers['Verify']
        if username not in self.users:
            socket.send(errors.UserNotExists().toResponse())
            return False
        elif verify != self.users[username]['verify']:
            socket.send(errors.WrongUserPassword().toResponse())
            return False
        else:
            for session_id_already in self.sessions:
                session = self.sessions[session_id_already]
                if 'username' in session and session['username'] == username:
                    socket.send(errors.DuplicateLogin().toResponse())
                    return False
            socket.send(Response(headers={'Session': session_id, 'Theme': self.users[username]['theme']}))
            return True

    def respond_logout(self, socket, request, session_id):
        socket.send(Response(headers={}))
        return True

    def respond_list(self, socket, request, session_id):
        socket.send(Response(content=json.dumps(self.sessions[session_id]["data_list"])))

    def respond_get(self, socket, request, session_id):
        task_id = request.headers['Task-id']
        for idx1, task_list in enumerate(self.sessions[session_id]["data_list"]):
            for idx2, task in enumerate(task_list):
                if task['id'] == task_id:
                    socket.send(Response(content=json.dumps(task)))
                    return
        socket.send(errors.TaskNotExists().toResponse())

    def respond_move(self, socket, request, session_id):
        task_id = request.headers['Task-id']
        from_index = int(request.headers['From'])
        to_index = int(request.headers['To'])
        if from_index not in [0, 1, 2] and to_index not in [0, 1, 2]:
            socket.send(errors.InvalidListIndex().toResponse())
            return
        if from_index == to_index:
            socket.send(errors.SameFromAndToList().toResponse())
            return
        for idx1, task_list in enumerate(self.sessions[session_id]["data_list"]):
            for idx2, task in enumerate(task_list):
                if task['id'] == task_id:
                    if idx1 == from_index:
                        self.lock.acquire()
                        del self.sessions[session_id]["data_list"][idx1][idx2]
                        self.sessions[session_id]["data_list"][to_index].append(task)
                        self.lock.release()
                        socket.send(Response(content=json.dumps(self.sessions[session_id]["data_list"])))
                        return
                    else:
                        socket.send(errors.TaskNotInTheList().toResponse())
                        return
        socket.send(errors.TaskNotExists().toResponse())

    def respond_add(self, socket, request, session_id):
        task_json = json.loads(request.content)
        if task_json['title'] == '':
            socket.send(errors.TaskTitleRequired().toResponse())
            return
        if self.check_task_json(task_json) is False:
            socket.send(errors.InvalidTaskJson().toResponse())
            return
        for idx1, task_list in enumerate(self.sessions[session_id]["data_list"]):
            for idx2, task in enumerate(task_list):
                if task['id'] == task_json['id']:
                    socket.send(errors.TaskIDAlreadyExists().toResponse())
                    return
        self.lock.acquire()
        self.sessions[session_id]["data_list"][0].insert(0, task_json)
        self.lock.release()
        socket.send(Response(content=json.dumps(self.sessions[session_id]["data_list"])))

    def respond_update(self, socket, request, session_id):
        task_json = json.loads(request.content)
        if self.check_task_json(task_json) is False:
            socket.send(errors.InvalidTaskJson().toResponse())
            return
        for idx1, task_list in enumerate(self.sessions[session_id]["data_list"]):
            for idx2, task in enumerate(task_list):
                if task['id'] == task_json['id']:
                    self.lock.acquire()
                    self.sessions[session_id]["data_list"][idx1][idx2] = task_json
                    self.lock.release()
                    socket.send(Response(content=json.dumps(self.sessions[session_id]["data_list"])))
                    return
        socket.send(errors.TaskNotExists().toResponse())

    def respond_archive(self, socket, request, session_id):
        self.lock.acquire()
        self.sessions[session_id]["data_list"][-1] = []
        self.lock.release()
        socket.send(Response(content=json.dumps(self.sessions[session_id]["data_list"])))

    def respond_theme(self, socket, request, session_id):
        username = self.sessions[session_id]["username"]
        self.lock.acquire()
        self.users[username]['theme'] = request.headers['Path']
        self.lock.release()
        self.save_user()
        socket.send(Response())

if __name__ == '__main__':
    with open('config/run_server_config.json') as f:
        config = json.load(f)
    Server(config['server_host'], config['server_port']).run()
