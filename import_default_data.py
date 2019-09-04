#coding=utf-8


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qa_web.settings")

import django
django.setup()

from main.models import *
import codecs
def import_location():
    f = open('Location.txt')
    txt = f.read()
    LocationList = []
    title = txt.split(',')
    print title
    for item in title:
        #print item
        start,end = map(int,item.split('-'))
        #print start,end
        print range(start,(end + 1))
        for number in range(start,(end + 1)):
            location = Location(name=number)
            LocationList.append(location)
    #location = Location(name=title)
    #LocationList.append(location)
    f.close()
    Location.objects.bulk_create(LocationList)

def import_Time_Bucket():
    Time_Bucket_list = []
    for hour in range(24):
        str_hour = str(hour).zfill(2)
        line_hour = str_hour + ":00-" + str_hour + ":59"
        print line_hour
        time_bucket = Time_Bucket(name = line_hour)
        Time_Bucket_list.append(time_bucket)
    Time_Bucket.objects.bulk_create(Time_Bucket_list)

def import_Department():
    f = open('Department.txt')
    txt = f.read()
    f.close()
    objectList = []
    title = txt.split('，')
    print title
    for item in title:
        department = Department(name=item)
        objectList.append(department)
    Department.objects.bulk_create(objectList)

def import_model(txt_file,model_object):
    f = open(txt_file)
    txt = f.read()
    f.close()
    objectList = []
    title = txt.split('，')
    print title
    for item in title:
        single_object = model_object(name=item)
        objectList.append(single_object)
    model_object.objects.bulk_create(objectList)

def import_hr_info():
    objectList = []
    f = open(u'人岗 按数据库department匹配名.csv')
    for line in f:
        item_list = line.split(',')
        employee_number, employee_name, department = item_list[0], item_list[1], item_list[2]
        department_id = Department.objects.get(name = department)
        single_object = hr_info(hr_employee_number = employee_number,
                               hr_employee_name = employee_name,
                               hr_department = department_id)
        objectList.append(single_object)
    f.close()
    hr_info.objects.bulk_create(objectList)

def import_hr_info_team():
    objectList = []
    f = codecs.open(u'人岗 按数据库department匹配名 含班组.csv', "r", "utf-8")
    # f = open(u'人岗 按数据库department匹配名 含班组.csv','r', 'utf-8')
    print f
    s = f.readlines()
    print s
    for line in s:
        print line
        item_list = line.split(',')
        employee_number, employee_name, department, team = item_list[0], item_list[1], item_list[2], item_list[3]
        if employee_number == u'\ufeff338747':
            employee_number = u'338747'
        department_id = Department.objects.get(name=department)
        employee_number = employee_number.zfill(8)

        print type(employee_number), employee_number
        team = team.strip()
        employee_number = employee_number.strip()
        print employee_number, team
        print type(team)
        print team == u'无'
        # print chardet.detect(team)
        # print chardet.detect(department)
        team_id = Team.objects.get(name=team)
        # print employee_number, team_id
        hr_object = hr_info.objects.get(hr_employee_number=employee_number)
        hr_object.hr_team = team_id
        # objectList.append(hr_object)
        hr_object.save()
    f.close()

if __name__ == "__main__":
    '''初始化时已完成
    import_location()
    import_Time_Bucket()
    import_Department()
    import_model("Information_Source.txt",Information_Source)
    import_model("Information_classification.txt", Information_classification)
    import_model("Event_class.txt", Event_class)
    import_model("Team.txt", Team)
    import_model("State.txt", State)
    '''
    import_hr_info()
    print('Done!')