#coding=utf-8
from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __unicode__(self):
        return self.name

class Time_Bucket(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __unicode__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __unicode__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __unicode__(self):
        return self.name

class Information_Source(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __unicode__(self):
        return self.name

class Information_classification(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __unicode__(self):
        return self.name

class Event_class(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __unicode__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50)

    def natural_key(self):
        return (self.name)

    class Meta:
        unique_together = (('name'),)

    def __unicode__(self):
        return self.name

class qa_info(models.Model):
    data = models.DateField(u'日期')
    location = models.ForeignKey(Location,verbose_name=u'地点')
    time_bucket = models.ForeignKey(Time_Bucket, verbose_name=u'时间')
    department = models.ForeignKey(Department, verbose_name=u'受检单位')
    team = models.ForeignKey(Team,default = u'无', verbose_name=u'责任班组')
    responsible_person = models.CharField(max_length=100, verbose_name=u'责任人')
    information_Source = models.ForeignKey(Information_Source, verbose_name=u'信息来源')
    information_classification = models.ForeignKey(Information_classification, verbose_name=u'问题分类')
    event_class = models.ForeignKey(Event_class, verbose_name=u'事件等级')
    problem_description = models.TextField(verbose_name = u'问题描述', unique_for_date = 'data')
    corrective_action = models.TextField(u'整改措施')
    treatment_suggestion = models.TextField(u'处理意见')
    state = models.ForeignKey(State, verbose_name=u'关闭情况')
    scrutator = models.CharField(max_length=100, verbose_name=u'检查者')
    Appendix = models.FileField(upload_to='upload/%Y/%m/%d',blank=True, verbose_name=u'相关附件')
    grade = models.DecimalField(max_digits=1, decimal_places=0,verbose_name = u'严重程度', blank= True, null=True)

    class Meta:
        ordering = ["-data"]

    def __unicode__(self):
        return self.problem_description

class hr_info(models.Model):
    hr_employee_number = models.CharField(max_length=100, verbose_name=u'员工编号')
    hr_employee_name = models.CharField(max_length=100, verbose_name=u'员工姓名')
    hr_department = models.ForeignKey(Department, blank= True, null=True,verbose_name=u'受检单位')
    hr_team = models.ForeignKey(Team, blank= True, null=True, verbose_name=u'责任班组')

    def __unicode__(self):
        return self.hr_employee_name