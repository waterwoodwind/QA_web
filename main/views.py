#coding=utf-8
from django.shortcuts import render
from main.models import qa_info
from django.core import serializers
import json
# Create your views here.
def home(request):
    exclude_list = [u"检查者", u"ID", u"相关附件"]

    query_data = qa_info.objects.all()
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
                u"sortable":u"true",
            }
            columns_set.append(columns_item)
            #print field.name, field.verbose_name
    print columns_set
    json_columns = json.dumps(columns_set)


    upload_data = []
    for item in list_data:
        upload_data.append(item['fields'])
        #print upload_data

    chinese_updata = []
    for item in upload_data:
        print item
        dict_updata = {}
        for key,value in item.items():
            if not dict_name_verbose_name[key] in exclude_list:
                dict_updata[dict_name_verbose_name[key]] = value

            #print chinese_updata
        chinese_updata.append(dict_updata)



    upload_data = json.dumps(chinese_updata)
    return render(request, 'home.html',{'json_data': upload_data,
                                        'json_columns': json_columns})