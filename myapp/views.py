from django.shortcuts import render, redirect
from .models import *
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Faculty authentication helpers
def is_faculty(user):
    return user.is_authenticated and hasattr(user, 'faculty_profile')
def index(request):
    return render(request, 'index.html')

def student_login(request):
    error=""
    if request.method == 'POST':
        
        # Handle login logic here
        data=Student.objects.all()
        name=request.POST.get('name')
        password=request.POST.get('password')
        print(name,password)
        try:
            student =Student.objects.get(name=name,password=password)
            print(student)
            request.session['student_id']=student.id
            return redirect('student_panel')

        except Student.DoesNotExist:
            error="Invalid name or password"
    return render(request,'student_login.html',{'error':error})


def student_panel(request):
    if 'student_id' not in request.session:
        return redirect('index')
    
    student=Student.objects.get(id=request.session['student_id'])

    return render(request,'student_panel.html',{'student':student})

def student_logout(request):
    if 'student_id' in request.session:
        del request.session['student_id']
    return redirect('index')

def edit_student(request):
    if 'student_id' not in request.session:
        return redirect('index')
    
    student=Student.objects.get(id=request.session['student_id'])
    error=""
    if request.method == 'POST':
        student.name=request.POST.get('name')
        student.password=request.POST.get('password')
        student.dob=request.POST.get('dob')
        student.roll_number=request.POST.get('roll_number')
        student.save()
        return redirect('student_panel')
    return render(request,'edit_student.html',{'student':student,'error':error})

def student_result(request):
    if 'student_id' not in request.session:
        return redirect('student_login')
    student = Student.objects.get(id=request.session['student_id'])
    results = Result.objects.filter(student=student)
    return render(request, 'student_result.html', {'results': results})



def student_attendance(request):
    if 'student_id' not in request.session:
        return redirect('student_login')

    student = Student.objects.get(id=request.session['student_id'])
    today = date.today()

    today_attendance = Attendances.objects.filter(
        student=student,
        date=date.today()
    )

    return render(
        request,
        'student_attendance.html',
        {
            'student': student,
            'today_attendance': today_attendance,
            'today': today,
        }
    )

def student_notice(request):
    if 'student_id' not in request.session:
        return redirect('student_login')
    student = Student.objects.get(id=request.session['student_id'])

    notices = Notice.objects.filter(
        department=student.department,
        semester=student.semester
    ).order_by('-date')

    return render(request, 'student_notice.html', {
        'student': student,
        'notices': notices
    })


def contact_faculty(request):
    if 'student_id' not in request.session:
        return redirect('student_login')
    student=Student.objects.get(id=request.session['student_id'])
    faculty_list=Faculty.objects.filter(department=student.department)
    return render(request,'contact_faculty.html',{'student':student,'faculty_list':faculty_list})

def send_message(request,faculty_id):
    if 'student_id' not in request.session:
        return redirect('student_login')
    student=Student.objects.get(id=request.session['student_id'])
    faculty=Faculty.objects.get(id=faculty_id)
    
    if request.method=='POST':
        message_text=request.POST['message']

        ContactMessage.objects.create(
            student=student,
            faculty=faculty,
            message=message_text
        )   
        return redirect('contact_faculty')
    return render(request,'send_message.html',{'student':student,'faculty':faculty})


def faculty_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'faculty_profile'):
            login(request, user)
            return redirect('faculty_dashboard')
        else:
            return render(request, 'faculty_login.html', {'error': 'Invalid credentials'})
    return render(request, 'faculty_login.html')

@login_required(login_url='/faculty/login/')
@user_passes_test(is_faculty, login_url='/faculty/login/')
def faculty_dashboard(request):
    faculty = request.user.faculty_profile
    return render(request, 'faculty_dashboard.html', {'faculty': faculty})

@login_required(login_url='/faculty/login/')
@user_passes_test(is_faculty, login_url='/faculty/login/')
def faculty_attendance(request):
    faculty = request.user.faculty_profile.faculty
    students = Student.objects.filter(department=faculty.department)
    lectures = Lectures.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        lecture_id = request.POST.get('lecture_id')
        present = request.POST.get('present') == 'on'
        date = request.POST.get('date')
        student = Student.objects.get(id=student_id)
        lecture = Lectures.objects.get(id=lecture_id)
        attendance, created = Attendances.objects.update_or_create(
            student=student, lecture=lecture, date=date,
            defaults={'present': present}
        )
    attendances = Attendances.objects.filter(student__department=faculty.department)
    return render(request, 'faculty_attendance.html', {
        'faculty': faculty,
        'students': students,
        'lectures': lectures,
        'attendances': attendances
    })

@login_required(login_url='/faculty/login/')
@user_passes_test(is_faculty, login_url='/faculty/login/')
def faculty_notice(request):
    faculty = request.user.faculty_profile.faculty
    notices = Notice.objects.filter(department=faculty.department)
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        semester = request.POST.get('semester')
        Notice.objects.create(
            title=title,
            message=message,
            department=faculty.department,
            semester=semester
        )
        return redirect('faculty_notice')
    return render(request, 'faculty_notice.html', {
        'faculty': faculty,
        'notices': notices
    })

@login_required(login_url='/faculty/login/')
@user_passes_test(is_faculty, login_url='/faculty/login/')
def faculty_messages(request):
    faculty = request.user.faculty_profile.faculty
    messages = ContactMessage.objects.filter(faculty=faculty).order_by('-date')
    return render(request, 'faculty_messages.html', {
        'faculty': faculty,
        'messages': messages
    })
