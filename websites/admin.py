from django.contrib import admin
from .models import Profiles,Attendance,Equipment,HistoryAttendance,MyModel

admin.site.register(Profiles)
# admin.site.register(Attendance)
admin.site.register(Equipment)
# admin.site.register(HistoryAttendance)
admin.site.register(MyModel)