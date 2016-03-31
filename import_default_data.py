#coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qa_web.settings")
from main.models import *

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

if __name__ == "__main__":
    import_location()
    import_Time_Bucket()
    import_Department()
    import_model("Information_Source.txt",Information_Source)
    import_model("Information_classification.txt", Information_classification)
    import_model("Event_class.txt", Event_class)
    import_model("Team.txt", Team)
    import_model("State.txt", State)
    print('Done!')