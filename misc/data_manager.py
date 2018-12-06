# coding: utf-8
import sys
sys.path.append('../')
from . import global_
from .const import sample_data_list
import json
from client import LoginClient, LoginedClient
from gui.error_popup import ErrorPopup
from gui.login_popup import LoginPopup
from . import utils

class DataManager(object):

    '''
    这个类负责处理数据和记录日志。
    当View中发出 添加/获取/删除 任务的请求后，会把请求发给这个类
    这个类负责和服务器通信，并把结果同步到自身的data_list中
    通信的结果有两种：
        通信成功，此时返回True，并且自身的data_list就是成功后的data_list
        通信失败，此时返回False，自身的data_list不做任何改变
    '''

    data_list = []

    def __init__(self, server_host, server_port):
        self.data_list = sample_data_list
        self.server_host = server_host
        self.server_port = server_port
        self.client = LoginClient(server_host, server_port)
        self.server_info = server_host + ':' + str(server_port)

    def __parse(self, request, response):
        global_.log_scroll_view.add_log(self.server_info, request)
        global_.log_scroll_view.add_log(self.server_info, response)
        if response.code == 200:
            self.data_list = json.loads(response.content)
            return True
        else:
            p = ErrorPopup()
            p.init(response)
            p.open()
            return False

    def require_login(self):
        p = LoginPopup()
        p.open()

    def login(self, username, password, login_popup):
        request, response = self.client.request_login(username, password)
        global_.log_scroll_view.add_log(self.server_info, request)
        global_.log_scroll_view.add_log(self.server_info, response)
        if response.code == 200:
            self.client = self.client.create_client()
            login_popup.dismiss()
            if not global_.show_force_no_sync:
                # for show
                global_.dm.sync_task()
            if 'Theme' in response.headers:
                global_.root_widget.root_layout.background_source = response.headers['Theme']
            utils.sync_dm_and_view()
        else:
            p = ErrorPopup()
            p.init(response)
            p.open()

    def sync_task(self):
        #  通信并更新data_list，失败返回False
        request, response = self.client.request_list()
        return self.__parse(request, response)

    def add_task(self, task_json):
        request, response = self.client.request_add(task_json)
        return self.__parse(request, response)

    def update_task(self, task_json):
        request, response = self.client.request_update(task_json)
        return self.__parse(request, response)

    def move_task(self, task_json, from_idx, to_idx):
        request, response = self.client.request_move(task_json['id'], from_idx, to_idx)
        return self.__parse(request, response)

    def archive_task(self):
        request, response = self.client.request_archive()
        return self.__parse(request, response)

    def change_theme(self, path):
        request, response = self.client.request_change_theme(path)
        global_.log_scroll_view.add_log(self.server_info, request)
        global_.log_scroll_view.add_log(self.server_info, response)
        if response.code == 200:
            # change theme here
            global_.root_widget.root_layout.background_source = path
            return True
        else:
            p = ErrorPopup()
            p.init(response)
            p.open()
            return False

    def logout_if_logined(self):
        if isinstance(self.client, LoginedClient):
            request, response = self.client.request_logout()
            print(str(request))
            print(str(response))

