from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

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

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class qa_info(models.Model):
    data = models.DateField('date')
    location = models.ForeignKey(Location)
    time_bucket = models.ForeignKey(Time_Bucket)
    department = models.ForeignKey(Department)
    responsible_person = models.CharField(max_length=100)
    information_Source = models.ForeignKey(Information_Source)
    information_classification = models.ForeignKey(Information_classification)
    event_class = models.ForeignKey(Event_class)
    problem_description = models.TextField()
    corrective_action = models.TextField()
    treatment_suggestion = models.TextField()
    state = models.ForeignKey(State)
    scrutator = models.CharField(max_length=100)
    Appendix = models.FileField(upload_to='upload/%Y/%m/%d')

    class Meta:
        ordering = ["data"]

    def __unicode__(self):
        return self.problem_description

