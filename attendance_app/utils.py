from datetime import datetime
from .models import AttendanceRecord

def get_workin_hours(time_in, time_out):
    if time_out:
        # return time_out - time_in
        return time_out.hour - time_in.hour - ((time_out.minute, time_out.second) < (time_in.minute, time_in_seconds))
    return 0

def get_total_working_hours(time_in, time_out):
    # getting total hours
    time_in_seconds = time_in.second if time_in else 0
    time_out_seconds = time_out.second if time_out else 0

    time_in_minutes = time_in.minute if time_in else 0
    time_out_minutes = time_out.minute if time_out else 0

    time_in_hours = time_in.hour if time_in else 0
    time_out_hours = time_out.hour if time_out else 0

    total_seconds = 60 - time_in_seconds + time_out_seconds
    # getting modulus
    seconds = total_seconds // 60
    # getting total minutes
    total_minute = (60 - time_in_minutes + time_out_minutes) + seconds
    minute = total_minute % 60
    total_hours = (time_out_hours - (time_in_hours + 1)) + total_minute // 60
    total_hours_work = round((total_hours + minute / 60), 2)

    return total_hours_work

def get_total_working_days():
    unique_dates = AttendanceRecord.objects.values('date').distinct()
    total_working_days = unique_dates.count()

    return total_working_days

def get_average_work_hours(total_work_hours, total_working_days):
    if total_working_days > 0:
        average_work_hours_per_day = total_work_hours / total_working_days
    else:
        average_work_hours_per_day = 0

    return average_work_hours_per_day