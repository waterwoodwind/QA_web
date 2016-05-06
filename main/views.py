#coding=utf-8
from django.shortcuts import render
from main.models import qa_info
from django.core import serializers
import json
# Create your views here.
def home(request):
    exclude_list = [u"检查者", u"责任人", u"ID", u"相关附件"]

    query_data = qa_info.objects.all().order_by('-id')
    json_data = serializers.serialize("json", query_data,use_natural_foreign_keys=True)
    list_data = json.loads(json_data)

    dict_name_verbose_name = {}
    columns_set = []
    for field in qa_info._meta.fields:
        dict_name_verbose_name[field.name] = field.verbose_name
        if not field.verbose_name in exclude_list:
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
    return render(request, 'home.html',{'json_data': upload_data,
                                        'json_columns': json_columns})