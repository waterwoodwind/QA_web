#coding=utf-8
import os
import sys
sys.path.append("F:\\github\\QA_web")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qa_web.settings")

import django
django.setup()

from main.models import *
from django.core import serializers
import json
import pandas as pd

exclude_list = [u"检查者", u"责任人", u"ID"]
query_data = qa_info.objects.all().order_by('-data')
json_data = serializers.serialize("json", query_data, use_natural_foreign_keys=True)
list_data = json.loads(json_data)
print list_data

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

df_data = pd.DataFrame(chinese_updata)
source = df_data[u"信息来源"].value_counts()
df_group =df_data.groupby(u"日期")
df_day_count = df_group.count()
date_index = ['2016-06-21', '2016-06-22']
df_day_count.loc[list_a_month].sum()

df_data = pd.DataFrame(chinese_updata)
df_da = pd.DataFrame(chinese_updata, index=df_data[u'日期'])
df_month = df_da.loc[list_a_month]
df_month[u"信息来源"].value_counts()












