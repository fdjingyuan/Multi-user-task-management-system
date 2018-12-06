#coding: utf-8
import sys
sys.path.append('../')
import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.app import runTouchApp
from misc import global_
from communication.response import Response
from communication.request import Request

Builder.load_file('kv/log_scroll_view.kv')


class LogLabel(Label):
    pass


class LogScrollView(ScrollView):
    def __init__(self, **kwargs):
        super(LogScrollView, self).__init__(**kwargs)
        self.gridlayout = LogGridLayout()
        self.gridlayout.bind(minimum_height=self.gridlayout.setter('height'))
        self.add_widget(self.gridlayout)
        self.scroll_to_bottom()
        global_.log_scroll_view = self

    def add_text(self, text):
        # 如果要添加新的log，需要通过这个方法添加
        self.gridlayout.add_widget(LogLabel(text=text))
        self.scroll_to_bottom()

    def add_log(self, server_info, request_or_response):
        print(str(request_or_response))
        self.add_text(request_or_response.toKivyLog(server_info))


    def scroll_to_bottom(self):
        # 将该视图滑动到最底部
        self.scroll_y = 0



class LogGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(LogGridLayout, self).__init__(**kwargs)
        self.cols = 1
