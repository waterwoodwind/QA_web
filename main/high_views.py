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
    df_group = df_month[u'受检单位'].groupby(df_month[u'信息来源']).value_counts().to_json()
    print df_group
    print type(df_group)
    '''
    team = df_month[u'受检单位'][df_month[u'信息来源']==u"班组自查"].value_counts().to_json()
    quality = df_month[u'受检单位'][df_month[u'信息来源']==u"车间监管"].value_counts().to_json()
    workshop = df_month[u'受检单位'][df_month[u'信息来源']==u"质量监管"].value_counts().to_json()
    json_data = {'team':team, 'quality': quality, 'workshop':workshop}
    json_data = json.dumps(json_data)
    '''
    return HttpResponse(df_group)