#coding: utf-8
# from kivy.config import Config
# Config.set('graphics', 'fullscreen', '0')
# Config.set('graphics', 'width', '550')
# Config.set('graphics', 'height', '500')
import sys
sys.path.append('../')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import (SettingsWithSidebar,
                               SettingsWithSpinner,
                               SettingsWithTabbedPanel)
from kivy.properties import OptionProperty, ObjectProperty, BooleanProperty

from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from misc import global_
from misc import utils
from kivy.app import runTouchApp
import uuid

Builder.load_file('kv/task_detail.kv')

class RootWidget(Widget):
    pass


class YearSpinner(Spinner):

    def __init__(self, **kwargs):
        super(YearSpinner, self).__init__(**kwargs)


class MonthSpinner(Spinner):

    def __init__(self, **kwargs):
        super(MonthSpinner, self).__init__(**kwargs)


class DaySpinner(Spinner):

    def __init__(self, **kwargs):
        super(DaySpinner, self).__init__(**kwargs)

    def on_press(self):
        year_spinner = self.panel.year_spinner
        month_spinner = self.panel.month_spinner
        if year_spinner.text != "" and month_spinner.text != "":
            year = int(year_spinner.text)
            month = int(month_spinner.text)
            day_num = utils.get_month_day(year, month)
            self.values = [""] + [str(x) for x in range(1, day_num + 1)]
        else:
            self.values = [""]


class ColorSelectionButton(Button):

    is_selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ColorSelectionButton, self).__init__(**kwargs)

    def on_press(self):
        color_buttons = self.panel.color_selections
        for color_button in color_buttons:
            color_button.is_selected = False
        self.is_selected = True

    def on_is_selected(self, instance, new_value):
        if new_value is True:
            self.text = "•"
        else:
            self.text = ""



class LeftLabel(Label):
    pass


class TaskDetailPanel(BoxLayout):

    def __init__(self, **kwargs):
        super(TaskDetailPanel, self).__init__(**kwargs)
        global_.task_panel = self


class TaskAddPopup(Popup):

    def add_task(self):
        task_json = {}
        task_json['id'] = str(uuid.uuid1())
        task_json['title'] = self.panel.title.text.decode('utf-8')
        if self.panel.year_spinner.text != "" and self.panel.month_spinner.text != "" and self.panel.day_spinner.text != "":
            task_json['date'] = {}
            task_json['date']['year'] = int(self.panel.year_spinner.text)
            task_json['date']['month'] = int(self.panel.month_spinner.text)
            task_json['date']['day'] = int(self.panel.day_spinner.text)
        for idx, color_button in enumerate(self.panel.color_selections):
            if color_button.is_selected is True:
                task_json['color_index'] = idx
                break
        if self.panel.detail_info.text != "":
            task_json['detail_info'] = self.panel.detail_info.text.decode('utf-8')
        if global_.dm.add_task(task_json) is True:
            self.dismiss()
            utils.sync_dm_and_view()

class TaskDetailPopup(Popup):

    def init_popup(self, task_json):
        self.task_json = task_json
        self.panel.title.text = task_json['title']
        if 'date' in task_json:
            self.panel.year_spinner.text = str(task_json['date']['year'])
            self.panel.month_spinner.text = str(task_json['date']['month'])
            self.panel.day_spinner.text = str(task_json['date']['day'])
        if 'color_index' in task_json:
            self.panel.color_selections[task_json['color_index']].is_selected = True
        if 'detail_info' in task_json:
            self.panel.detail_info.text = task_json['detail_info']

    def update_task(self):
        task_json = {'id': self.task_json['id']}
        task_json['title'] = self.panel.title.text.decode('utf-8')
        if self.panel.year_spinner.text != "" and self.panel.month_spinner.text != "" and self.panel.day_spinner.text != "":
            task_json['date'] = {}
            task_json['date']['year'] = int(self.panel.year_spinner.text)
            task_json['date']['month'] = int(self.panel.month_spinner.text)
            task_json['date']['day'] = int(self.panel.day_spinner.text)
        for idx, color_button in enumerate(self.panel.color_selections):
            if color_button.is_selected is True:
                task_json['color_index'] = idx
                break
        if self.panel.detail_info.text != "":
            task_json['detail_info'] = self.panel.detail_info.text.decode('utf-8')
        if global_.dm.update_task(task_json) is True:
            self.dismiss()
            utils.sync_dm_and_view()

if __name__ == '__main__':
    # runTouchApp(TaskDetailPanel())
    TestApp().run()