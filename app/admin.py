from django.contrib import admin
from app.models import *

admin.site.register(CustomUser)
admin.site.register(Grade)
# admin.site.register(Attendance)
# admin.site.register(Mark)
admin.site.register(School)
admin.site.register(TeacherGrades)
admin.site.register(Mark)
