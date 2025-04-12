from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # ✅ Step 12
import csv

from .models import Student, Attendance


# Home view to resolve the error
def home(request):
    return render(request, 'attendance/home.html')  # Ensure that 'home.html' exists in your templates directory.
def mark_attendance(request):
    # your logic here
    return render(request, 'attendance/mark_attendance.html')



# ✅ STEP 12: Require login for attendance report
@login_required
def attendance_report(request):
    students = Student.objects.all()
    selected_student = request.GET.get('student')
    selected_date = request.GET.get('date')

    filters = Q()
    if selected_student:
        filters &= Q(student__id=selected_student)
    if selected_date:
        filters &= Q(date=selected_date)

    records = Attendance.objects.filter(filters).order_by('-date')
    return render(request, 'attendance/attendance_report.html', {
        'records': records,
        'students': students,
        'selected_student': selected_student,
        'selected_date': selected_date,
    })


# ✅ STEP 11 + 12: CSV Export protected by login
@login_required
def export_attendance_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student', 'Date', 'Status'])

    selected_student = request.GET.get('student')
    selected_date = request.GET.get('date')

    filters = Q()
    if selected_student:
        filters &= Q(student__id=selected_student)
    if selected_date:
        filters &= Q(date=selected_date)

    records = Attendance.objects.filter(filters).order_by('-date')

    for record in records:
        writer.writerow([record.student.name, record.date, record.status])

    return response
