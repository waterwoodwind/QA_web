#coding=utf-8
import pandas as pd
import pickle
import json
from main.models import qa_info
from django.core import serializers
from django.http import HttpResponse
import os

#function
def list_all_data():
    file_1 = file('data_all.pkl', 'rb')
    updata = pickle.load(file_1)
    return updata

#views
def refresh_middle_data(request):
    if os.path.exists('data_all.pkl'):
        os.remove('data_all.pkl')
    if os.path.exists('data.h5'):
        os.remove('data.h5')

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



    return HttpResponse(u"前端数据已刷新")