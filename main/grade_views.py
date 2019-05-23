#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from main.models import qa_info
from django.core import serializers
import json
import pandas as pd
import arrow
import re

from views import df_chinese_data
from save_load_func import list_all_data
from func_for_grade_views import get_qa_info_with_grade
from func_for_grade_views import get_hr_info

def staff_grade_year(request):
    df_data = get_qa_info_with_grade()
    # 获取输入时间，对df_data按时间截取一次
    # 创建name_grade_department_list
    list_hr_info = get_hr_info()

    # 人员list for 循环
    for i,element in enumerate(list_hr_info):
        name = element[0]

        # 对单人进行分数计算，取出df_data中包含该人全部行df_single_person
        # 对df_single_person合并总分
        # 人名、总分、部门压入name_grade_department_list
    return render(request, 'source_month_stack.html')