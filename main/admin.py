from django.contrib import admin
from main.models import Location
from main.models import Time_Bucket
from main.models import qa_info
from main.models import *
# Register your models here.


admin.site.register(qa_info)
admin.site.register(Location)
admin.site.register(Time_Bucket)
admin.site.register(Department)
admin.site.register(Team)
admin.site.register(Information_Source)
admin.site.register(Information_classification)
admin.site.register(Event_class)
admin.site.register(State)