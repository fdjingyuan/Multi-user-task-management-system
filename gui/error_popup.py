#coding: utf-8
import sys
sys.path.append('../')
import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import runTouchApp


Builder.load_file('kv/error_popup.kv')

class ErrorPopup(Popup):
    msg = StringProperty("ERROR")

    def init(self, response):
        self.msg = str(response)


if __name__ == '__main__':
    runTouchApp(ErrorPopup())
