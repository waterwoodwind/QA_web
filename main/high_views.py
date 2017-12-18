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

def numpy_to_int(dict_np):
    for key,item in dict_np.items():
        dict_np[key] = int(item)

    return dict_np

# Create your views here.
def source_month_stack(request):
    return render(request, 'source_month_stack.html')

def ajax_source_month_stack(request):
    df_data = pd.read_hdf('data.h5', 'df')
    df_da = pd.DataFrame(list_all_data(), index=df_data[u'日期'])
    year_month = request.GET.get('value_conf', None)

    end = arrow.get(year_month)
    end = end.replace(day=25)
    start = end.replace(months=-1)
    start = start.replace(day=26)
    print end
    list_a_month = []
    for r in arrow.Arrow.range('day', start, end):
        a_day = r.format('YYYY-MM-DD')
        list_a_month.append(a_day)
    df_month = df_da.loc[list_a_month]

    team = df_month[u'受检单位'][df_month[u'信息来源']==u"班组自查"].value_counts().to_dict()
    workshop = df_month[u'受检单位'][df_month[u'信息来源']==u"车间监管"].value_counts().to_dict()
    quality = df_month[u'受检单位'][df_month[u'信息来源']==u"质量监管"].value_counts().to_dict()
    team = numpy_to_int(team)
    quality = numpy_to_int(quality)
    workshop = numpy_to_int(workshop)
    
    json_data = {'team':team, 'quality': quality, 'workshop':workshop}
    json_data = json.dumps(json_data)


    return HttpResponse(json_data)


def team_month_stack(request):
    return render(request, 'team_month_stack.html')


def ajax_team_month_stack(request):
    df_data = pd.read_hdf('data.h5', 'df')
    df_da = pd.DataFrame(list_all_data(), index=df_data[u'日期'])
    year_month = request.GET.get('value_conf', None)

    end = arrow.get(year_month)
    end = end.replace(day=25)
    start = end.replace(months=-1)
    start = start.replace(day=26)
    print end
    list_a_month = []
    for r in arrow.Arrow.range('day', start, end):
        a_day = r.format('YYYY-MM-DD')
        list_a_month.append(a_day)
    df_month = df_da.loc[list_a_month]

    team = df_month[u'责任班组'][df_month[u'信息来源']==u"班组自查"].value_counts().to_dict()
    workshop = df_month[u'责任班组'][df_month[u'信息来源']==u"车间监管"].value_counts().to_dict()
    quality = df_month[u'责任班组'][df_month[u'信息来源'] == u"质量监管"].value_counts().to_dict()
    team = numpy_to_int(team)
    workshop = numpy_to_int(workshop)
    quality = numpy_to_int(quality)

    json_data = {'team':team, 'quality': quality, 'workshop':workshop}
    json_data = json.dumps(json_data)


    return HttpResponse(json_data)


def self_inspect_trendence(request, workshop_name):
    if workshop_name == "1":
        list_team_name = [u'航线一（1）', u'航线一（2）', u'航线一（3）', u'航线一（4）']
    else:
        list_team_name = [u'航线二（1）', u'航线二（2）', u'航线二（3）', u'航线二（4）']
    df_data = pd.read_hdf('data.h5', 'df')
    df_da = pd.DataFrame(list_all_data(), index=df_data[u'日期'])
    string_index = df_data[u'日期']
    # 计算出起止月份
    start_day = string_index.min()
    end_day = string_index.max()
    start_ar = arrow.get(start_day)
    end_ar = arrow.get(end_day)
    print end_ar

    if start_ar.day >= 26:
        number_month = start_ar.month + 1
    else:
        number_month = start_ar.month
    start_month = start_ar.replace(month=number_month)
    if end_ar.day >= 26:
        number_month = end_ar.month + 1
    else:
        number_month = end_ar.month + 1
    end_month = end_ar.replace(months=number_month)
    print end_month

    list_month = []

    dict_data = {}
    for item in list_team_name:
        dict_data[item] = { 'total': [],'percent':[]}
    for r in arrow.Arrow.range('month', start_month, end_month):
        year_month = r.format("YYYY-MM")
        end = arrow.get(r)
        end = end.replace(day=25)
        start = end.replace(months=-1)
        start = start.replace(day=26)
        list_a_month = []
        for r in arrow.Arrow.range('day', start, end):
            a_day = r.format('YYYY-MM-DD')
            list_a_month.append(a_day)
        try:
            df_month = df_da.loc[list_a_month]
            list_month.append(year_month)
            for item in list_team_name:
                df_month_airline_1 = df_month[df_month[u'责任班组']==item]
                total_count = df_month_airline_1.shape[0]
                dict_data[item]['total'].append(total_count)
                df_month_self_inspect_count = df_month_airline_1[df_month_airline_1[u'信息来源']==u'班组自查']
                self_inspect_count = df_month_self_inspect_count.shape[0]
                percent = 100*self_inspect_count/total_count
                dict_data[item]['percent'].append(percent)
        except:
            continue

    json_month = json.dumps(list_month)
    json_team_name = json.dumps(list_team_name)
    json_data = json.dumps(dict_data)
    return render(request, 'self_inspect_trendence.html',{"json_month":json_month,
                                                            "json_team_name":json_team_name,
                                                          "json_data":json_data})

def grade_scatter(request):
    df_data = pd.read_hdf('data.h5', 'df')
    df_data = df_data[df_data[u"严重程度"]>0]
    df_data = df_data[[u"日期",u"受检单位",u"严重程度"]]
    df_airline_1 = df_data[df_data[u"受检单位"]==u"航线一"]
    json_airline_1 = df_airline_1[[u"日期",u"严重程度"]].to_json(orient="values")
    df_airline_2 = df_data[df_data[u"受检单位"]==u"航线二"]
    json_airline_2 = df_airline_2[[u"日期",u"严重程度"]].to_json(orient="values")
    df_certain = df_data[df_data[u"受检单位"]==u"定检"]
    json_certain = df_certain[[u"日期",u"严重程度"]].to_json(orient="values")
    df_other = df_data[(df_data[u"受检单位"]<>u"航线一")&(df_data[u"受检单位"]<>u"航线二")&(df_data[u"受检单位"]<>u"定检")]
    json_other = df_other[[u"日期",u"严重程度"]].to_json(orient="values")
    return render(request, 'grade_scatter.html',{"json_airline_1": json_airline_1,
                                                 "json_airline_2":json_airline_2,
                                                 "json_certain":json_certain,
                                                 "json_other":json_other})