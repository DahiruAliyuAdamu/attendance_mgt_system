from django.urls import path
from .views import *

app_name = 'attendance'

urlpatterns = [
    path('', HomeView.as_view(), name='dashboard'),
    path('register/', RegisterEmployeeView.as_view(), name='register_employee'),
    path('mark-attendance/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('view-attendance/', ViewAttendanceReportView.as_view(), name='view_attendance_report'),
]