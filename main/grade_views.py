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
from views import date_range_df_chinese_data
from save_load_func import list_all_data
from func_for_grade_views import get_qa_info_with_grade
from func_for_grade_views import df_to_gradedf
from func_for_grade_views import get_hr_info
from func_for_grade_views import get_hr_info_df

def staff_grade_year(request):
    if request.method == 'POST':
        post_data = request.POST
        date_range = post_data["date_range"]
        date_start = date_range.split(' to ')[0]
        date_end = date_range.split(' to ')[1]
        print date_start,date_end
        df_data = pd.DataFrame(date_range_df_chinese_data(date_start,date_end))
        df_data = df_data[df_data[u"严重程度"] > 0]
        df_data = df_data.loc[:, [u"责任人", u"检查者", u"严重程度"]]
        df_data[[u"严重程度"]] = df_data[[u"严重程度"]].apply(pd.to_numeric)

    else:
        df_data = get_qa_info_with_grade()

    if df_data.empty:
        return HttpResponse(u"该时间范围内无数据，请返回上一页")


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
            sum_single_person = int(sum_single_person)
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
            sum_single_person = int(sum_single_person)
        # 人名、总分、部门压入name_grade_department_list
            single_dict = {}
            single_dict[u"检查者"] = name
            single_dict[u"部门"] = department
            single_dict[u"检查分"] = sum_single_person
            name_grade_department_list.append(single_dict)
    #print name_grade_department_list
    json_grade = json.dumps(name_grade_department_list)
    return render(request, 'strutator_grade.html', {'json_grade': json_grade})

def department_grade(request):
    df_data = get_qa_info_with_grade()
    #print df_data
    # 获取输入时间，对df_data按时间截取一次
    # 创建name_grade_department_list
    person_grade_list = []
    list_hr_info = get_hr_info()
    df_hr_info = get_hr_info_df()
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
            sum_single_person = int(sum_single_person)

            # 人名、总分、部门压入name_grade_department_list
            person_grade_list.append(100 - sum_single_person)
        else:
            person_grade_list.append(100)
        # print name_grade_department_list
    df_hr_info[u'安全分'] = person_grade_list
    df_agg = df_hr_info.groupby(u'部门').agg('mean').round(2)
    print df_agg,type(df_agg)
    df_agg = df_agg.reset_index()
    df_dict = df_agg.to_dict('records')
    print df_dict
    json_grade = json.dumps(df_dict)
    # 班组分数
    df_team_mean = df_hr_info.groupby(u'班组').agg('mean').round(2)
    print df_team_mean
    df_team_mean_reset = df_team_mean.reset_index()
    dict_team_mean = df_team_mean_reset.to_dict('records')
    print dict_team_mean
    team_mean = json.dumps(dict_team_mean)
    return render(request, 'department_grade.html', {'json_grade': json_grade,
                                                     'json_team':team_mean})


def self_checking_grade(request):
    df_data = get_qa_info_with_grade()
    #print df_data
    # 获取输入时间，对df_data按时间截取一次
    # 创建name_grade_department_list
    person_grade_list = []
    list_hr_info = get_hr_info()
    df_hr_info = get_hr_info_df()
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
            sum_single_person = int(sum_single_person)

            # 人名、总分、部门压入name_grade_department_list
            person_grade_list.append(sum_single_person)
        else:
            person_grade_list.append(0)
        # print name_grade_department_list
    df_hr_info[u'安全分'] = person_grade_list
    df_scrutator = df_hr_info[df_hr_info[u'安全分']>0]
    df_agg = df_scrutator.groupby(u'部门').agg('mean').round(2)
    df_agg = df_agg.reset_index()
    df_dict = df_agg.to_dict('records')
    json_grade = json.dumps(df_dict)
    # 班组分数
    df_team_mean = df_scrutator.groupby(u'班组').agg('mean').round(2)
    df_team_mean_reset = df_team_mean.reset_index()
    dict_team_mean = df_team_mean_reset.to_dict('records')
    team_mean = json.dumps(dict_team_mean)
    return render(request, 'department_grade.html', {'json_grade': json_grade,
                                                     'json_team':team_mean})