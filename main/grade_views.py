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
    #print df_data
    # 获取输入时间，对df_data按时间截取一次
    # 创建name_grade_department_list
    name_grade_department_list = []
    list_hr_info = get_hr_info()

    # 人员list for 循环
    for i,element in enumerate(list_hr_info):
        sum_single_person = 0
        name = element[1]
        department = element[2]
        #print i, name
        # 对单人进行分数计算，取出df_data中包含该人全部行df_single_person
        df_single_person = df_data[df_data[u"责任人"]==name]
        if not df_single_person.empty:
            #print df_single_person
        # 对df_single_person合并总分
            sum_single_person = df_single_person[u"严重程度"].sum()
            sum_single_person = sum_single_person.astype(int)
            print name,sum_single_person
            print type(sum_single_person)
        # 人名、总分、部门压入name_grade_department_list
            single_dict = {}
            single_dict[u"责任人"] = name
            single_dict[u"部门"] = department
            single_dict[u"安全分"] = 100 - sum_single_person
            name_grade_department_list.append(single_dict)
    #print name_grade_department_list
    json_grade = json.dumps(name_grade_department_list)
    return render(request, 'staff_grade_year.html', {'json_grade': json_grade})


def strutator_grade(request):
    df_data = get_qa_info_with_grade()
    #print df_data
    # 获取输入时间，对df_data按时间截取一次
    # 创建name_grade_department_list
    name_grade_department_list = []
    list_hr_info = get_hr_info()

    # 人员list for 循环
    for i,element in enumerate(list_hr_info):
        sum_single_person = 0
        name = element[1]
        department = element[2]
        #print i, name
        # 对单人进行分数计算，取出df_data中包含该人全部行df_single_person
        df_single_person = df_data[df_data[u"检查者"]==name]
        if not df_single_person.empty:
            #print df_single_person
        # 对df_single_person合并总分
            sum_single_person = df_single_person[u"严重程度"].sum()
            sum_single_person = sum_single_person.astype(int)
            print name,sum_single_person
            print type(sum_single_person)
        # 人名、总分、部门压入name_grade_department_list
            single_dict = {}
            single_dict[u"检查者"] = name
            single_dict[u"部门"] = department
            single_dict[u"检查分"] = sum_single_person
            name_grade_department_list.append(single_dict)
    #print name_grade_department_list
    json_grade = json.dumps(name_grade_department_list)
    return render(request, 'strutator_grade.html', {'json_grade': json_grade})