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


def numpy_to_int(dict_np):
    for key,item in dict_np.items():
        dict_np[key] = int(item)

    return dict_np

# Create your views here.
def source_month_stack(request):
    return render(request, 'source_month_stack.html')

def ajax_source_month_stack(request):
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
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
    quality = df_month[u'受检单位'][df_month[u'信息来源']==u"车间监管"].value_counts().to_dict()
    workshop = df_month[u'受检单位'][df_month[u'信息来源']==u"质量监管"].value_counts().to_dict()
    team = numpy_to_int(team)
    quality = numpy_to_int(quality)
    workshop = numpy_to_int(workshop)
    
    json_data = {'team':team, 'quality': quality, 'workshop':workshop}
    json_data = json.dumps(json_data)


    return HttpResponse(json_data)


def team_month_stack(request):
    return render(request, 'team_month_stack.html')


def ajax_team_month_stack(request):
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
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
    quality = df_month[u'责任班组'][df_month[u'信息来源']==u"车间监管"].value_counts().to_dict()
    workshop = df_month[u'责任班组'][df_month[u'信息来源']==u"质量监管"].value_counts().to_dict()
    team = numpy_to_int(team)
    quality = numpy_to_int(quality)
    workshop = numpy_to_int(workshop)

    json_data = {'team':team, 'quality': quality, 'workshop':workshop}
    json_data = json.dumps(json_data)


    return HttpResponse(json_data)