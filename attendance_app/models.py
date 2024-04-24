from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # photo = models.ImageField(upload_to='employee_photos')

    def __str__(self) -> str:
        return f"{self.name} - {self.employee_id}"

class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(null=True, blank=True)
    break_time = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"Attendance Record for Employee ID {self.employee_id} on {self.date}"