#coding: utf-8
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '768')
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from functools import partial
from gui.background_popup import BackGroundPopup
from misc import global_
from kivy.lang import Builder
import json
from gui.task_detail import TaskAddPopup
from misc.data_manager import DataManager
from misc import utils

Builder.load_file('kv/main.kv')




class RootLayout(GridLayout):

    bottom_layout = ObjectProperty(None)
    command_on = False
    background_source = StringProperty("")

    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)

    def __archive_lastlist_onebyone(self, dt=None):
        list_view = global_.task_lists[-1]
        if len(list_view.adapter.data) != 0:
            list_view.adapter.data = list_view.adapter.data[1:]
            list_view._trigger_reset_populate()
            Clock.schedule_once(self.__archive_lastlist_onebyone, 0.2)

    def archived_list(self):
        # 归档list
        if global_.dm.archive_task() is True:
            self.__archive_lastlist_onebyone()

    def __refresh_list_onebyone(self, list_view_index, dt=None):
        if list_view_index < len(global_.task_lists):
            list_view = global_.task_lists[list_view_index]
            list_data = global_.dm.data_list[list_view_index]
            if len(list_view.adapter.data) < len(list_data):
                list_view.adapter.data.append(list_data[len(list_view.adapter.data)])
                list_view._trigger_reset_populate()
            else:
                list_view_index += 1
            Clock.schedule_once(partial(self.__refresh_list_onebyone, list_view_index), 0.05)

    def refresh_list(self):
        # 刷新
        if global_.dm.sync_task() is True:
            for i in range(len(global_.dm.data_list)):
                global_.task_lists[i].adapter.data = []
                global_.task_lists[i]._trigger_reset_populate()
            self.__refresh_list_onebyone(0)

    def open_background_popup(self):
        p = BackGroundPopup()
        p.root_layout = self
        p.open()

    def toggle_command(self):
        if self.command_on is False:
            self.bottom_layout.size_hint_y = 0.7
            self.command_on = True
        else:
            self.command_on = False
            self.bottom_layout.size_hint_y = 0.000000001

    def add_task_popup(self):
        p = TaskAddPopup()
        p.open()


class RootWidget(Widget):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)


class MainApp(App):

    def build(self):
        global_.root_widget = RootWidget()
        return global_.root_widget

    def on_start(self):
        print('On start(May be sync task):')
        global_.dm.require_login()
        # global_.dm.sync_task()
        # utils.sync_dm_and_view()

    def on_stop(self):
        global_.dm.logout_if_logined()

if __name__ == '__main__':
    with open('config/run_client_config.json') as f:
        config = json.load(f)
    global_.dm = DataManager(config['server_host'], config['server_port'])
    global_.show_force_no_sync = True
    MainApp().run()
