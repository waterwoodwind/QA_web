#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from main.models import qa_info
from django.core import serializers
import json
import pandas as pd
import arrow
import re
import pickle
#time count
import time
# import save and load data function
from save_load_func import list_all_data

def timeit(func):
    def wrapper(*args, **args2):
        start = time.clock()
        back = func(*args, **args2)
        end =time.clock()
        print "@%.3fs taken for {%s}" % (end - start, func.__name__)
        return back
    return wrapper

# Create functions here.
def make_scrutator_json(df_data, department, source):
    df_da = df_data[(df_data[u"受检单位"] == department)& \
                    (df_data[u"信息来源"] == source)]
    df_person = df_da[u'责任人']
    #chinese_name = u'([/u4e00-/u9fa5]+)'
    #pattern = re.compile(chinese_name)
    res_dict = {}
    for item in df_person.values:
        #print item
        results = re.findall(ur"[\u4e00-\u9fa5]+", item)
        for result in results:
            #print result
            res_dict[result] = res_dict.get(result, 0) + 1

    #检查者
    df_scrutator = df_da[u"检查者"]
    res_dict = {}
    for item in df_scrutator.values:
        # print item
        results = re.findall(ur"[\u4e00-\u9fa5]+", item)
        for result in results:
            # print result
            res_dict[result] = res_dict.get(result, 0) + 1
    scrutator_count_list = res_dict.items()

    json_list = []

    for item in scrutator_count_list:
        single_dict = {}
        # 去掉人员名单中的无
        if item[0] == u'无':
            print item[0], item[1]
            continue
        single_dict[u'检查者'] = item[0]
        single_dict[u'次数'] = item[1]
        json_list.append(single_dict)
    json_scrutator = json.dumps(json_list)
    return json_scrutator

def make_month_count_json():
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
    return json_month, json_count

# Create your views here.
@timeit
def home(request):
    if request.method == 'POST':
        post_data = request.POST
        date_range = post_data["date_range"]
        date_start = date_range.split(' to ')[0]
        date_end = date_range.split(' to ')[1]
        print date_start,date_end
        df_data = pd.DataFrame(date_range_df_chinese_data(date_start,date_end))
    else:

        df_data = pd.read_hdf('data.h5', 'df')

    if df_data.empty:
        return HttpResponse(u"该时间范围内无数据，请返回上一页")


    air1_dep = make_scrutator_json(df_data, u"航线一", u"车间监管")
    air1_team = make_scrutator_json(df_data, u"航线一", u"班组自查")
    air2_dep = make_scrutator_json(df_data, u"航线二", u"车间监管")
    air2_team = make_scrutator_json(df_data, u"航线二", u"班组自查")
    air3_dep = make_scrutator_json(df_data, u"航线三", u"车间监管")
    air3_team = make_scrutator_json(df_data, u"航线三", u"班组自查")
    certain_dep = make_scrutator_json(df_data, u"定检", u"车间监管")
    certain_team = make_scrutator_json(df_data, u"定检", u"班组自查")

    #
    json_month, json_count = make_month_count_json()
    return render(request, "home.html", {'air1_dep': air1_dep,
                                         'air1_team': air1_team,
                                         'air2_dep':air2_dep,
                                         'air2_team':air2_team,
                                         'air3_dep': air3_dep,
                                         'air3_team': air3_team,
                                         'certain_dep':certain_dep,
                                         'certain_team':certain_team,
                                         "json_month":json_month,
                                        "json_count":json_count})

@timeit
def information(request):
    upload_data = json.dumps(list_all_data())
    return render(request, 'information.html',{'json_data': upload_data})

@timeit
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

    #save list
    file_1 = file('data_all.pkl', 'wb')
    pickle.dump(chinese_updata, file_1, True)
    #save pd file
    df_data = pd.DataFrame(chinese_updata)
    df_data.to_hdf('data.h5', 'df')
    return chinese_updata


def return_df_chinese_data():
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


@timeit
def background(request):
    upload_data = json.dumps(return_df_chinese_data())
    return render(request, 'background.html', {'json_data': upload_data})

@timeit
def source(request):
    df_data = pd.read_hdf('data.h5', 'df')
    source = df_data[u"信息来源"].value_counts().to_json()
    title = u'汇总'
    return render(request, 'source.html',{'title': title, 'source': source})

@timeit
def source_month(request):
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
    source = df_month[u"信息来源"].value_counts().to_json()
    print source
    print type(source)
    return HttpResponse(source)

@timeit
def month_count(request):
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
        number_month = end_ar.month
    else:
        number_month = end_ar.month
    end_month = end_ar.replace(months=number_month)
    print end_month

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

@timeit
def classification(request):
    df_data = pd.read_hdf('data.h5', 'df')
    df_da = pd.DataFrame(list_all_data(), index=df_data[u'日期'])
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
        number_month = end_ar.month + 1
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
            list_cl_name = [u'程序执行', u'工卡执行', u'工具设备', u"维护作风", u"现场管理", u"维修记录", u"生产组织", u"器材管理", u"其它"]
            for item in list_cl_name:
                dict_cl.setdefault(item, 0)
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
    #获取最后一个元素，控制显示
    dict_selected = {}
    for index, list_item in enumerate(list_month_cl_count):
        for item, value in list_item.items():
            dict_selected[item] = False
            if index == (len(list_month_cl_count) - 1):
                dict_selected[item] = True

    json_month = json.dumps(list_month)
    json_count = json.dumps(dict_selected)
    json_series = json.dumps(all_series)
    return render(request, "classification.html",{"json_month":json_month,
                                               "json_count":json_count,
                                                  "json_series": json_series})

@timeit
def person_count(request):
    if request.method == 'POST':
        post_data = request.POST
        date_range = post_data["date_range"]
        date_start = date_range.split(' to ')[0]
        date_end = date_range.split(' to ')[1]
        print date_start,date_end
        df_data = pd.DataFrame(date_range_df_chinese_data(date_start,date_end))
    else:
        df_data = pd.read_hdf('data.h5', 'df')

    if df_data.empty:
        return HttpResponse(u"该时间范围内无数据，请返回上一页")

    df_da = df_data
    df_person = df_da[u'责任人']
    #chinese_name = u'([/u4e00-/u9fa5]+)'
    #pattern = re.compile(chinese_name)
    res_dict = {}
    for item in df_person.values:
        #print item
        results = re.findall(ur"[\u4e00-\u9fa5]+", item)
        for result in results:
            #print result
            res_dict[result] = res_dict.get(result, 0) + 1
    person_count_list = res_dict.items()
    json_list = []

    for item in person_count_list:
        single_dict = {}
        # 去掉人员名单中的无
        if item[0] == u'无':
            print item[0], item[1]
            continue
        single_dict[u'责任人'] = item[0]
        single_dict[u'次数'] = item[1]
        json_list.append(single_dict)
    json_person = json.dumps(json_list)

    #检查者
    df_scrutator = df_da[u"检查者"]
    res_dict = {}
    for item in df_scrutator.values:
        # print item
        results = re.findall(ur"[\u4e00-\u9fa5]+", item)
        for result in results:
            # print result
            res_dict[result] = res_dict.get(result, 0) + 1
    scrutator_count_list = res_dict.items()

    json_list = []

    for item in scrutator_count_list:
        single_dict = {}
        # 去掉人员名单中的无
        if item[0] == u'无':
            print item[0], item[1]
            continue
        single_dict[u'检查者'] = item[0]
        single_dict[u'次数'] = item[1]
        json_list.append(single_dict)
    json_scrutator = json.dumps(json_list)
    return render(request, "person_count.html", {'json_person': json_person,
                                                 'json_scrutator':json_scrutator})

@timeit
def date_range_df_chinese_data(date_start, date_end):
    exclude_list = []

    query_data = qa_info.objects.filter(data__range=[date_start, date_end]).order_by('-data')
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

@timeit
def month_count_group_by_source(request):
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
    list_month_count_quality = []
    list_month_count_workshop = []
    list_month_count_team = []

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
            list_month_count_quality.append(df_month[u'信息来源'][df_month[u'信息来源']==u"质量监管"].count())
            list_month_count_workshop.append(df_month[u'信息来源'][df_month[u'信息来源']==u"车间监管"].count())
            list_month_count_team.append(df_month[u'信息来源'][df_month[u'信息来源']==u"班组自查"].count())
        except:
            continue

    json_month = json.dumps(list_month)
    json_count_quality = json.dumps(list_month_count_quality)
    json_count_workshop = json.dumps(list_month_count_workshop)
    json_count_team = json.dumps(list_month_count_team)
    return render(request, "month_count_group_by_source.html",{"json_month":json_month,
                                                            "json_count_quality":json_count_quality,
                                                               "json_count_workshop":json_count_workshop,
                                                               "json_count_team":json_count_team})

@timeit
def month_count_group_by_department(request):
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
    list_month_count_scheduled = []
    list_month_count_airline1 = []
    list_month_count_airline2 = []

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
            list_month_count_scheduled.append(df_month[u'受检单位'][df_month[u'受检单位']==u"定检"].count())
            list_month_count_airline1.append(df_month[u'受检单位'][df_month[u'受检单位']==u"航线一"].count())
            list_month_count_airline2.append(df_month[u'受检单位'][df_month[u'受检单位']==u"航线二"].count())
        except:
            continue

    json_month = json.dumps(list_month)
    json_count_scheduled = json.dumps(list_month_count_scheduled)
    json_count_airline1 = json.dumps(list_month_count_airline1)
    json_count_airline2 = json.dumps(list_month_count_airline2)
    return render(request, "month_count_group_by_department.html",{"json_month":json_month,
                                                            "json_count_scheduled":json_count_scheduled,
                                                               "json_count_airline1":json_count_airline1,
                                                               "json_count_airline2":json_count_airline2})