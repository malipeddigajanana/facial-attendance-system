from django.shortcuts import render
from .models import Employee, Attendance
import face_recognition
import cv2

def home(request):
    # Dummy view to show all employees
    employees = Employee.objects.all()
    return render(request, 'attendance/home.html', {'employees': employees})

def mark_attendance(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    
    # Open webcam for facial recognition
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    # Convert the image from BGR to RGB
    rgb_frame = frame[:, :, ::-1]

    # Find all face locations in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

    if face_locations:
        # If a face is detected, mark attendance
        Attendance.objects.create(employee=employee, status='Present')
    else:
        Attendance.objects.create(employee=employee, status='Absent')

    video_capture.release()
    return render(request, 'attendance/home.html', {'message': 'Attendance marked!'})
