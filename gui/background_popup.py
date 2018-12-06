# coding: utf-8
import sys
sys.path.append('../')
import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.app import runTouchApp
from misc import global_

Builder.load_file('kv/background_popup.kv')

class BackGroundPopup(Popup):
    pass


class BackGroundCard(FloatLayout):
    button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BackGroundCard, self).__init__(**kwargs)

    def on_press(self):
        global_.dm.change_theme(self.background_path)
        # self.popup.root_layout.background_source = self.background_path
        self.popup.dismiss()

if __name__ == '__main__':
    runTouchApp(BackGroundPopup())