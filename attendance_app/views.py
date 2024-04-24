from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractWeek
import calendar
from .models import Employee, AttendanceRecord
from .forms import EmployeeForm
from .utils import *

class HomeView(View):
    template_name = 'attendance/index.html'

    def get(self, request):
        return render(request, self.template_name)

class RegisterEmployeeView(LoginRequiredMixin, View):
    def get(self, request):
        form = EmployeeForm()
        return render(request, 'attendance/register_employee.html', {'form': form})

    def post(self, request):
        form = EmployeeForm(request.POST)
        print(form)
        if form.is_valid():
            print('success')
            staff = form.save(commit=False)
            staff.save()

            return JsonResponse({'status': 'success', 'message': 'register successful', 'id': staff.employee_id})
        return JsonResponse({'status': 'error', 'message': 'An error occured'})
        
class MarkAttendanceView(LoginRequiredMixin, View):
    def get(self, request):
        # Logic for capturing images, face detection, recognition, and rendering form
        return render(request, 'attendance/mark_attendance.html')

    def post(self, request):
        employee_id = request.POST['employee_id']
        print(employee_id)
        
        # Logic for capturing images, face detection, recognition, and recording attendance
        action = request.POST.get('action')
        print(action)
        if not employee_id or not action:
            return JsonResponse({'status': 'error', 'message': 'Employee ID and action are required'})

        employee = Employee.objects.filter(employee_id=employee_id).first()
        if not employee:
            return JsonResponse({'status': 'error', 'message': f'Employee with {employee_id} ID does not exists'})
        
        attendance_record = AttendanceRecord.objects.filter(employee_id=employee, date=datetime.now().date()).first()
        
        if action == 'time_in':
            if attendance_record and attendance_record.time_in:
                return JsonResponse({'status': 'error', 'message': 'Time-in already marked for today'})
            else:
                AttendanceRecord.objects.create(employee=employee, time_in=datetime.now())
                return JsonResponse({'status': 'success', 'message': 'Time-in marked successfully'})

        elif action == 'break_time':
            if not attendance_record or not attendance_record.time_in:
                return JsonResponse({'status': 'error', 'message': 'Time-in must be marked before break time'})
            elif attendance_record.break_time:
                return JsonResponse({'status': 'error', 'message': 'Break time already marked for today'})
            else:
                attendance_record.break_time = datetime.now()
                attendance_record.save()
                return JsonResponse({'status': 'error', 'message': 'Break time marked successfully'})

        elif action == 'time_out':
            if not attendance_record or not attendance_record.time_in:
                return JsonResponse({'status': 'error', 'message': 'Time-in must be marked before time-out'})
            elif attendance_record.time_out:
                return JsonResponse({'status': 'error', 'message': 'Time-out already marked for today'})
            else:
                attendance_record.time_out = datetime.now()
                attendance_record.save()
                return JsonResponse({'status': 'success', 'message': 'Time-out marked successfully'})
        return JsonResponse({'status': 'success', 'message': 'register successful'})

class ViewAttendanceReportView(LoginRequiredMixin, View):
    def get(self, request):
        # Logic for generating attendance reports
        attendance_records = AttendanceRecord.objects.all()
        total_employees = Employee.objects.count()
        attendance_data = AttendanceRecord.objects.all().order_by('date')

        average_work_hours = 0
        for record in attendance_records:
            average_work_hours += get_total_working_hours(record.time_in, record.time_out)
        total_working_days = get_total_working_days()
        
        # Preparing data for Chart.js
        dates = []
        attendance_counts = []

        # Calculate attendance count for each date
        current_date = None
        count = 0
        for record in attendance_data:
            if record.date != current_date:
                if current_date is not None:
                    dates.append(current_date.strftime('%Y-%m-%d'))
                    attendance_counts.append(count)
                current_date = record.date
                count = 1
            else:
                count += 1

        # Append the last date's count
        if current_date is not None:
            dates.append(current_date.strftime('%Y-%m-%d'))
            attendance_counts.append(count)

        attendance_counts_by_month = AttendanceRecord.objects.annotate(
            month=ExtractMonth('date')
        ).values('month').annotate(
            attendance_count=Count('id')
        ).order_by('month')

        months_list = []
        attendance_counts_list = []

        # Iterate over the queryset and extract values into lists
        for entry in attendance_counts_by_month:
            # Extract month and attendance count from each entry
            month_number = entry['month']
            attendance_count = entry['attendance_count']
            
            # Convert month number to month name
            month_name = calendar.month_name[month_number]

            months_list.append(month_name)
            attendance_counts_list.append(attendance_count)

        context = {
            'attendance_records': attendance_records,
            'total_employees': total_employees,
            'total_working_days': total_working_days,
            'average_work_hours': average_work_hours,

            'dates': dates,
            'attendance_counts': attendance_counts,

            'months': months_list,
            'attendance_counts': attendance_counts_list,
        }
        return render(request, 'attendance/view_attendance_report.html', context)
