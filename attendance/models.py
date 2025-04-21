from django.db import models

class Attendance(models.Model):
    student_id = models.CharField(max_length=20)
    status = models.CharField(max_length=10)  # Present / Absent
    date = models.DateField()       

    def __str__(self):
        return f"{self.student_id} - {self.status}"
