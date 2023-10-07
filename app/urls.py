from django.urls import path, include
from app.views import *

urlpatterns = [
    path('', index, name='index'),
    path('notifications/', notifications, name='notifications'),
    path('teacher-details/', teacher_details, name='teacher-details'),
    path('student-details/<int:id>/', student_details, name='student-details'),
    path('students/', students, name='students'),
    path('filter-class/<int:id>/', filter_class, name='filter-class'),
    path('user/', user, name='user'),
    path('student-login/', loginPage, name='student-login'),
    path('teacher-login/', TeacherLoginPage, name='teacher-login'),
    path('add_user/', registerPage, name='add_user'),
    path('marksheet/', marksheet, name='marksheet'),
    path('teachers-grade/', teachers_grade, name='teachers-grade'),
    path('test/', test, name='test'),
    # path('attendance/', attendance, name='attendance'),
    # path('attendance_d/<int:id>/', attendance_details, name='attendance-d'),
]
