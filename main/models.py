#coding=utf-8
from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = '地点'
        verbose_name_plural = '地点'

    def __unicode__(self):
        return self.name

class Time_Bucket(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Information_Source(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Information_classification(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Event_class(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class qa_info(models.Model):
    data = models.DateField('日期')
    location = models.ForeignKey(Location,verbose_name='地点')
    time_bucket = models.ForeignKey(Time_Bucket, verbose_name='时间')
    department = models.ForeignKey(Department, verbose_name='受检单位')
    team = models.ForeignKey(Team,default = u'无', verbose_name='责任班组')
    responsible_person = models.CharField(max_length=100, verbose_name='责任人')
    information_Source = models.ForeignKey(Information_Source, verbose_name='信息来源')
    information_classification = models.ForeignKey(Information_classification, verbose_name='问题分类')
    event_class = models.ForeignKey(Event_class, verbose_name='事件等级')
    problem_description = models.TextField('问题描述')
    corrective_action = models.TextField('整改措施')
    treatment_suggestion = models.TextField('处理意见')
    state = models.ForeignKey(State, verbose_name='关闭情况')
    scrutator = models.CharField(max_length=100, verbose_name='检查者')
    Appendix = models.FileField(upload_to='upload/%Y/%m/%d',blank=True, verbose_name='相关附件')

    class Meta:
        ordering = ["data"]

    def __unicode__(self):
        return self.problem_description

