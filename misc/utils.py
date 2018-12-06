# coding: utf-8
import calendar
import time
from . import global_
import hashlib

def get_month_day(year, month):
    return calendar.monthrange(year, month)[1]


def get_year_list():
    year = time.localtime(time.time()).tm_year
    return ["", str(year), str(year + 1)]


def get_year():
    return time.localtime(time.time()).tm_year


def is_beyond_ddl(date):
    dt = time.localtime(time.time())
    now_year = dt.tm_year
    now_month = dt.tm_mon
    now_day = dt.tm_mday

    if 'year' not in date:
        year = get_year()
    else:
        year = date['year']
    month = date['month']
    day = date['day']

    if year < now_year:
        return True
    if (year == now_year) and (month < now_month):
        return True
    if (year == now_year) and (month == now_month) and (day < now_day):
        return True
    return False


def get_date_display(date):
    dt_str = "→ "
    now_year = get_year()
    if date['year'] != now_year:
        dt_str += str(date['year'])[-2:] + '.'
    dt_str += str(date['month']) + '.'
    dt_str += str(date['day'])
    dt_str += "  截止"
    return dt_str



def sync_dm_and_view():
    '''
    将dm中的task_list和view中的data做同步
    '''
    for i, task_list in enumerate(global_.task_lists):
        task_list.adapter.data = global_.dm.data_list[i]
        task_list._trigger_reset_populate()


def get_md5(string):
    string = str(string)
    m2 = hashlib.md5()
    m2.update(string)
    return str(m2.hexdigest())
 

