# coding: utf-8
import sys
sys.path.append('../')
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListView, SelectableView
from collections import defaultdict
from kivy.lang import Builder
from .task_detail import TaskDetailPopup
from misc import global_
import json
from misc import utils

Builder.load_file('kv/task_list_view.kv')


class TaskItem(BoxLayout, Button, SelectableView):
    def __init__(self, **kwargs):
        super(TaskItem, self).__init__(**kwargs)


class MyListItemButtonMock(TaskItem):
    meta = ObjectProperty(defaultdict(str))

    def __init__(self, meta, origin_item, origin_list_view, **kwargs):
        super(MyListItemButtonMock, self).__init__(**kwargs)
        self.meta = meta
        self.origin_item = origin_item
        self.origin_list_view = origin_list_view

    def on_touch_up(self, touch):
        # 只要放鼠标，所有的按钮都不应该有is_dragging
        collided_view = None
        for list_view in global_.task_lists:
            if list_view.collide_point(*touch.pos):
                collided_view = list_view
                break
        if collided_view is not None and collided_view != self.origin_list_view:
            for i in range(len(global_.task_lists)):
                if self.origin_list_view == global_.task_lists[i]:
                    origin_list_index = i
            for i in range(len(global_.task_lists)):
                if collided_view == global_.task_lists[i]:
                    collided_list_index = i
            if global_.dm.move_task(self.meta, origin_list_index, collided_list_index) is True:
                utils.sync_dm_and_view()
        return super(MyListItemButtonMock, self).on_touch_up(touch)




class MyListItemButton(TaskItem):

    meta = ObjectProperty(defaultdict(str))

    def __init__(self, meta, list_view_index=-1, list_view=None, **kwargs):
        # self.background_normal = 'data/img/pixel.png'
        super(MyListItemButton, self).__init__(**kwargs)
        self.meta = meta
        self.list_view_index = list_view_index
        self.list_view = list_view

    is_dragging = False
    moved = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.moved = False
            self.center_x = touch.pos[0]
            self.center_y = touch.pos[1]
            self.is_dragging = True

            window_pos = self.to_window(*touch.pos)
            self.added = MyListItemButtonMock(
                meta=self.meta,
                origin_item=self,
                origin_list_view=self.list_view,
                pos=[
                    window_pos[0] - self.width / 2,
                    window_pos[1] - self.height / 2
                ], size=[self.width, self.height])
            global_.root_widget.add_widget(
                self.added
            )

        return super(MyListItemButton, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        # 为了防止鼠标移动过快的情况，这里不使用collide_point，而是设置一个is_dragging属性
        # 只要有这个属性，那么就进行移动
        if self.is_dragging:
            self.moved = True
            self.center_x = touch.pos[0]
            self.center_y = touch.pos[1]

            window_pos = self.to_window(*touch.pos)
            self.added.center_x = window_pos[0]
            self.added.center_y = window_pos[1]

        return super(MyListItemButton, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        # 只要放鼠标，所有的按钮都不应该有is_dragging
        if self.is_dragging:
            self.is_dragging = False
            # 删除
            global_.root_widget.remove_widget(self.added)
            self.list_view._trigger_reset_populate()
            if self.moved is False:
                p = TaskDetailPopup()
                p.init_popup(self.meta)
                p.open()
        return super(MyListItemButton, self).on_touch_up(touch)




class ListItem(Button, BoxLayout):

    def __init__(self, **kwargs):
        super(ListItem, self).__init__(**kwargs)


class MyListView(BoxLayout):

    data_list = ObjectProperty([])

    def __init__(self, **kwargs):
        super(MyListView, self).__init__(**kwargs)

        self.list_adapter = ListAdapter(
            data=self.data_list,
            args_converter=self.converter,
            selection_mode='single',
            allow_empty_selection=True,
            cls=MyListItemButton)

        self.list_adapter.bind(on_selection_change=self.selection_change)
        self.list_view = ListView(adapter=self.list_adapter)

        #  滑动bar
        self.list_view.container.parent.bar_color = [1, 1, 1, 0.7]
        self.list_view.container.parent.bar_inactive_color = [1, 1, 1, 0.3]
        self.list_view.container.parent.bar_width = 3
        self.list_view.container.parent.bar_margin = 0

        self.add_widget(self.list_view)

        global_.task_lists.append(self.list_view)

    def selection_change(self, adapter, *args):
        if (adapter.selection):
            selected_obj = adapter.selection[0]            

    def refresh(self, new_data_list):
        self.list_view.adapter.data = new_data_list
        self.list_view._trigger_reset_populate()

    def on_data_list(self, instance, new_data_list):
        self.refresh(new_data_list)

    def converter(self, row_index, obj):
        kwargs = {}
        kwargs['meta'] = obj
        kwargs['list_view_index'] = row_index
        kwargs['list_view'] = self.list_view
        return kwargs




class SingleListWrapper(BoxLayout):

    list_name = StringProperty("")
    data_list = ObjectProperty([])

    def __init__(self, **kwargs):
        super(SingleListWrapper, self).__init__(**kwargs)
