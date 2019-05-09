#coding:utf-8
from django.contrib import admin
from main.models import Location
from main.models import Time_Bucket
from main.models import qa_info
from main.models import *
import re

# Register your models here.
class qa_infoAdmin(admin.ModelAdmin):
    list_display = ('data', 'problem_description', 'grade',)
    list_display_links = ('data', 'problem_description', 'grade',)
    def save_model(self, request, obj, form, change):
        filename = r'grade.csv'
        pos = []
        dict_grade = {}
        dict_grade.setdefault('找不到', )
        f_txt = open(filename, 'r')
        f_txt.readline()
        for line in f_txt:
            lines = line.decode("gb2312").split(',')
            #print lines[0], lines[1]
            pos.append(lines)
            dict_grade[lines[0].encode("utf-8")] = lines[1]
        f_txt.close()
        description = obj.problem_description
        print description
        description = description.encode("utf-8")
        print description
        result = re.search(r'【.*】', description)
        if result:
            des = result.group()
            print result.group()
            des = des.lstrip(r'【')
            des = des.rstrip(r'】')
            print des
            if dict_grade.get(des):
                obj.grade = dict_grade[des]
                print des.encode('gb2312')
        else:
            print ' NO MATCH'

        print obj.grade
        obj.save()

admin.site.register(qa_info, qa_infoAdmin)
admin.site.register(Location)
admin.site.register(Time_Bucket)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Information_Source)
admin.site.register(Information_classification)
admin.site.register(Event_class)
admin.site.register(State)