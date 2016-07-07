#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from main.models import qa_info
from django.core import serializers
import json
import pandas as pd
import arrow
# Create your views here.
def home(request):
    exclude_list = [u"检查者", u"责任人", u"ID"]

    query_data = qa_info.objects.all().order_by('-data')
    json_data = serializers.serialize("json", query_data,use_natural_foreign_keys=True)
    list_data = json.loads(json_data)

    dict_name_verbose_name = {}
    columns_set = []
    colheaders = []
    dataSchema = {}
    for field in qa_info._meta.fields:
        dict_name_verbose_name[field.name] = field.verbose_name

        if not field.verbose_name in exclude_list:
            print field.verbose_name
            colheaders.append(field.verbose_name.encode("utf8"))
            dataSchema[field.verbose_name] = ''
            columns_item = {
                u"title": field.verbose_name,
                u"field": field.verbose_name,
                #u"sortable": u"true",
            }
            if field.verbose_name == u"问题描述":
                columns_item[u"width"] = u"20%"
                columns_item[u"title"] = u"问题描述"
            elif field.verbose_name == u"整改措施":
                columns_item[u"width"] = u"20%"
                columns_item[u"title"] = u"整改措施"
            elif field.verbose_name == u"处理意见":
                columns_item[u"width"] = u"6%"
                columns_item[u"title"] = u"处理意见"
            else:
                split_list = list(field.verbose_name)
                # every two word add
                title_str = ""
                for i in range(len(split_list)):
                    title_str = title_str + split_list[i]
                    if (i+1)%2 == 0:
                        title_str = title_str + u"<br>"
                if field.verbose_name == u"相关附件":
                    columns_item[u'formatter'] = "attachment"
                columns_item[u"title"] = title_str
                columns_item[u"width"] = u"2%"
            columns_set.append(columns_item)


    json_columns = json.dumps(columns_set)


    upload_data = []
    for item in list_data:
        upload_data.append(item['fields'])
        #print upload_data

    chinese_updata = []
    for item in upload_data:
        dict_updata = {}
        for key,value in item.items():
            if not dict_name_verbose_name[key] in exclude_list:
                dict_updata[dict_name_verbose_name[key]] = value

            #print chinese_updata
        chinese_updata.append(dict_updata)

    upload_data = json.dumps(chinese_updata)
    return render(request, 'home.html',{'json_data': upload_data})

def df_chinese_data():
    exclude_list = []

    query_data = qa_info.objects.all().order_by('-data')
    json_data = serializers.serialize("json", query_data, use_natural_foreign_keys=True)
    list_data = json.loads(json_data)

    dict_name_verbose_name = {}
    columns_set = []
    colheaders = []
    dataSchema = {}
    for field in qa_info._meta.fields:
        dict_name_verbose_name[field.name] = field.verbose_name

        if not field.verbose_name in exclude_list:
            print field.verbose_name
            colheaders.append(field.verbose_name.encode("utf8"))
            dataSchema[field.verbose_name] = ''
            columns_item = {
                u"title": field.verbose_name,
                u"field": field.verbose_name,
                # u"sortable": u"true",
            }
            if field.verbose_name == u"问题描述":
                columns_item[u"width"] = u"20%"
                columns_item[u"title"] = u"问题描述"
            elif field.verbose_name == u"整改措施":
                columns_item[u"width"] = u"20%"
                columns_item[u"title"] = u"整改措施"
            elif field.verbose_name == u"处理意见":
                columns_item[u"width"] = u"6%"
                columns_item[u"title"] = u"处理意见"
            else:
                split_list = list(field.verbose_name)
                # every two word add
                title_str = ""
                for i in range(len(split_list)):
                    title_str = title_str + split_list[i]
                    if (i + 1) % 2 == 0:
                        title_str = title_str + u"<br>"
                if field.verbose_name == u"相关附件":
                    columns_item[u'formatter'] = "attachment"
                columns_item[u"title"] = title_str
                columns_item[u"width"] = u"2%"
            columns_set.append(columns_item)

    json_columns = json.dumps(columns_set)

    upload_data = []
    for item in list_data:
        single_data = item['fields']
        single_data[u'id'] = item['pk']
        upload_data.append(single_data)
        # print upload_data

    chinese_updata = []
    for item in upload_data:
        dict_updata = {}
        for key, value in item.items():
            dict_updata[dict_name_verbose_name[key]] = value

            # print chinese_updata
        chinese_updata.append(dict_updata)

    return chinese_updata

def background(request):


    upload_data = json.dumps(df_chinese_data())
    return render(request, 'background.html', {'json_data': upload_data})

def source(request):
    df_data = pd.DataFrame(df_chinese_data())
    source = df_data[u"信息来源"].value_counts().to_json()
    title = u'汇总'
    return render(request, 'source.html',{'title': title, 'source': source})

def source_month(request):
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
    source = df_month[u"信息来源"].value_counts().to_json()
    title = u'月'
    return HttpResponse(source)

def month_count(request):
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
    string_index = df_data[u'日期']
    # 计算出起止月份
    start_day = string_index.min()
    end_day = string_index.max()
    start_ar = arrow.get(start_day)
    end_ar = arrow.get(end_day)
    if start_ar.day >= 26:
        number_month = start_ar.month + 1
    else:
        number_month = start_ar.month
    start_month = start_ar.replace(month=number_month)
    if end_ar.day >= 26:
        number_month = end_ar.month + 1
    else:
        number_month = end_ar.month
    end_month = end_ar.replace(month=number_month)

    list_month = []
    list_month_count = []

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
            list_month_count.append(df_month[u'日期'].count())
        except:
            continue

    json_month = json.dumps(list_month)
    json_count = json.dumps(list_month_count)
    return render(request, "month_count.html",{"json_month":json_month,
                                               "json_count":json_count})

def classification(request):
    df_data = pd.DataFrame(df_chinese_data())
    df_da = pd.DataFrame(df_chinese_data(), index=df_data[u'日期'])
    string_index = df_data[u'日期']
    # 计算出起止月份
    start_day = string_index.min()
    end_day = string_index.max()
    start_ar = arrow.get(start_day)
    end_ar = arrow.get(end_day)
    if start_ar.day >= 26:
        number_month = start_ar.month + 1
    else:
        number_month = start_ar.month
    start_month = start_ar.replace(month=number_month)
    if end_ar.day >= 26:
        number_month = end_ar.month + 1
    else:
        number_month = end_ar.month
    end_month = end_ar.replace(month=number_month)

    list_month = []
    list_month_cl_count = []

    for r in arrow.Arrow.range('month', start_month, end_month):
        year_month = r.format("YYYY-MM").encode("utf-8")
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

            df_month_group = df_month.groupby(u'问题分类')
            df_cl = df_month_group[u"时间"].count()
            dict_cl = df_cl.to_dict()
            single_month = [dict_cl[u'程序执行'], dict_cl[u'工卡执行'], dict_cl[u'工具设备'], dict_cl[u"维护作风"], dict_cl[u"现场管理"],
                            dict_cl[u"维修记录"], dict_cl[u"生产组织"], dict_cl[u"器材管理"], dict_cl[u"其它"]]
            single_month = map(lambda x: int(x), single_month)

            list_month.append(year_month)
            list_month_cl_count.append({year_month : single_month})
        except:
            continue

    series_single_orignal = {
        "name": '2016-05',
        "type": 'bar',
        "data":[21,33,56,89,44,55,66],
        "itemStyle": {
            "normal":{
                "label":{
                    "show": "true",
                    "formatter": '{c}'
                }
            }
        }
    }
    all_series = []
    for list_item in list_month_cl_count:
        for item, value in list_item.items():
            print item, value
            series_single = series_single_orignal.copy()
            series_single["name"] = item
            series_single["data"] = value
            print series_single["name"], series_single["data"]
            all_series.append(series_single)
            print all_series
    json_month = json.dumps(list_month)
    json_count = json.dumps(list_month_cl_count)
    json_series = json.dumps(all_series)
    return render(request, "classification.html",{"json_month":json_month,
                                               "json_count":json_count,
                                                  "json_series": json_series})