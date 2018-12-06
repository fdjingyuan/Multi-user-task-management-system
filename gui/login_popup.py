#coding: utf-8
import sys
sys.path.append('../')
import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import runTouchApp
from misc import global_

Builder.load_file('kv/login_popup.kv')

class ErrorLoginPopup(Popup):
    pass

class LoginPopup(Popup):

    def on_login(self):
    	global_.dm.login(self.username.text, self.password.text, self)


if __name__ == '__main__':
    runTouchApp(LoginPopup())
