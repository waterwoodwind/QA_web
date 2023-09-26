#coding:utf-8
import re

filename = r'grade.csv'
pos = []
dict_grade = {}
dict_grade.setdefault('找不到',)
f_txt = open(filename, 'r')
f_txt.readline()
for line in f_txt:
    lines = line.decode("gb2312").split(',')
    print(lines[0], lines[1])
    pos.append(lines)
    dict_grade[lines[0].encode("utf-8")] = lines[1]
f_txt.close()
#对正则表达式取值
description = r'【工作结束后未清理现场】某年某月机号'
result = re.search(r'【.*】', description)
if result:
    des = result.group()
    print(result.group())
    des = des.lstrip(r'【')
    des = des.rstrip(r'】')
    
    print(dict_grade[des])
else:
    print(' NO MATCH')
