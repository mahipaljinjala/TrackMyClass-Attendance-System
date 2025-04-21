from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Attendance
from openpyxl import Workbook

def index(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        date = request.POST.get('date')

        if student_id and status and date:  # ✅ Added basic validation
            Attendance.objects.create(student_id=student_id, status=status, date=date)
            return render(request, 'attendance/index.html', {'success': '✔️ Attendance marked successfully!'})

    return render(request, 'attendance/index.html')

def view_attendance(request):
    date_filter = request.GET.get('date')  # ✅ Allow filtering by date
    records = Attendance.objects.all().order_by('date')

    if date_filter:
        records = records.filter(date=date_filter)

    return render(request, 'attendance/view_attendance.html', {'records': records, 'date_filter': date_filter})

def search_attendance(request):
    student_id = request.GET.get('student_id')
    records = Attendance.objects.none()  # ✅ Use None for empty queryset

    if student_id:
        records = Attendance.objects.filter(student_id=student_id).order_by('date')

    return render(request, 'attendance/search_attendance.html', {'records': records, 'student_id': student_id})

def export_attendance_excel(request):
    student_id = request.GET.get('student_id')
    records = Attendance.objects.all().order_by('-date')

    if student_id:
        records = records.filter(student_id=student_id)

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance Records"
    ws.append(['Student ID', 'Status', 'Date'])

    for record in records:
        ws.append([record.student_id, record.status, str(record.date)])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="attendance.xlsx"'
    wb.save(response)
    return response

@require_POST
def delete_attendance(request, record_id):
    record = get_object_or_404(Attendance, id=record_id)
    record.delete()
    return redirect(request.META.get('HTTP_REFERER', 'view_attendance'))
