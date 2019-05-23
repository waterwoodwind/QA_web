#coding=utf-8
import pandas as pd
from main.models import hr_info
from main.models import Department
from main.models import Team

def get_qa_info_with_grade():
    df_data = pd.read_hdf('data.h5', 'df')
    df_data = df_data[df_data[u"严重程度"] > 0]
    df_data = df_data.loc[:, [u"责任人",u"检查者", u"严重程度"]]
    return df_data

def get_hr_info():
    tuple_hr_info = list(hr_info.objects.values_list('hr_employee_number', 'hr_employee_name', 'hr_department', 'hr_team'))
    list_hr_info = []
    for i,item in enumerate(tuple_hr_info):
        element = []
        element.append(tuple_hr_info[i][0])
        element.append(tuple_hr_info[i][1])
        if item[2] <> None:
            element.append(Department.objects.get(id = item[2]).name)
        else:
            element.append(item[2])
        if item[3] <> None:
            element.append(Team.objects.get( id = item[3]).name)
        else:
            element.append(item[3])

        list_hr_info.append(element)
    return list_hr_info