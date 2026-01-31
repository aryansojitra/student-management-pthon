
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
    path('faculty/login/', faculty_login, name='faculty_login'),
    path('faculty/dashboard/', faculty_dashboard, name='faculty_dashboard'),
    path('faculty/attendance/', faculty_attendance, name='faculty_attendance'),
    path('faculty/notice/', faculty_notice, name='faculty_notice'),
    path('faculty/messages/', faculty_messages, name='faculty_messages'),
]
