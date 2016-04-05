from django.shortcuts import render
from main.models import qa_info
from django.core import serializers
import json
# Create your views here.
def home(request):
    query_data = qa_info.objects.all()
    json_data = serializers.serialize("json", query_data,use_natural_foreign_keys=True)
    list_data = json.loads(json_data)
    upload_data = []
    for item in list_data:
        upload_data.append(item['fields'])

    upload_data = json.dumps(upload_data)

    return render(request, 'home.html',{'json_data': upload_data})