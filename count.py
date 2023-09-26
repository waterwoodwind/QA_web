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

exclude_list = ["检查者", "责任人", "ID"]
query_data = qa_info.objects.all().order_by('-data')
json_data = serializers.serialize("json", query_data, use_natural_foreign_keys=True)
list_data = json.loads(json_data)
print(list_data)

dict_name_verbose_name = {}
columns_set = []
colheaders = []
dataSchema = {}
for field in qa_info._meta.fields:
    dict_name_verbose_name[field.name] = field.verbose_name

    if not field.verbose_name in exclude_list:
        print(field.verbose_name)
        colheaders.append(field.verbose_name.encode("utf8"))
        dataSchema[field.verbose_name] = ''
        columns_item = {
            "title": field.verbose_name,
            "field": field.verbose_name,
            #u"sortable": u"true",
        }
        if field.verbose_name == "问题描述":
            columns_item["width"] = "20%"
            columns_item["title"] = "问题描述"
        elif field.verbose_name == "整改措施":
            columns_item["width"] = "20%"
            columns_item["title"] = "整改措施"
        elif field.verbose_name == "处理意见":
            columns_item["width"] = "6%"
            columns_item["title"] = "处理意见"
        else:
            split_list = list(field.verbose_name)
            # every two word add
            title_str = ""
            for i in range(len(split_list)):
                title_str = title_str + split_list[i]
                if (i+1)%2 == 0:
                    title_str = title_str + "<br>"
            if field.verbose_name == "相关附件":
                columns_item['formatter'] = "attachment"
            columns_item["title"] = title_str
            columns_item["width"] = "2%"
        columns_set.append(columns_item)


json_columns = json.dumps(columns_set)


upload_data = []
for item in list_data:
    upload_data.append(item['fields'])
    #print upload_data

chinese_updata = []
for item in upload_data:
    dict_updata = {}
    for key,value in list(item.items()):
        if not dict_name_verbose_name[key] in exclude_list:
            dict_updata[dict_name_verbose_name[key]] = value

        #print chinese_updata
    chinese_updata.append(dict_updata)

df_data = pd.DataFrame(chinese_updata)
df_da = pd.DataFrame(chinese_updata, index=df_data['日期'])
df_group = df_da.groupby('问题分类')
df_classification =  df_group["时间"].count()
dict_cl = df_classification.to_dict()
single_month = [dict_cl['程序执行'], dict_cl['工卡执行'], dict_cl['工具设备'], dict_cl["维护作风"], dict_cl["现场管理"], dict_cl["维修记录"], dict_cl["生产组织"], dict_cl["器材管理"], dict_cl["其它"]]













