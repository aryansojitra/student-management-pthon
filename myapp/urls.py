
from django.urls import path

from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('student/login/',student_login,name='student_login'),
    path('student/panel/',student_panel,name='student_panel'),
    path('student/logout/',student_logout,name='student_logout'),
    path('student/edit/',edit_student,name='edit_student'),
    path('student/results/',student_result,name='student_result'),
    path('student/attendance/',student_attendance,name='student_attendance'),
    path('student/notice/',student_notice,name='student_notice'),
    path('student/contact-faculty/',contact_faculty,name='contact_faculty'),
    path('student/send-message/<int:faculty_id>/',send_message,name='send_message'),
]
