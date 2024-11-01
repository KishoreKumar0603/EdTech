from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from .models import *
from .forms import *

#

from django.contrib.auth import logout

#home page View
# def home(request):
#     student_username = request.session.get('student_user', None)
#     user= Student.objects.get(username=student_username)
#     context = {
#         'student_username': user.first_name.capitalize()
#     }
#     return render(request,'course/home/home.html',context)

def home(request):
    student_username = request.session.get('student_user', None)
    if not student_username:
        return render(request, 'course/home/home.html', context=None)
    try:
        user = Student.objects.get(username=student_username)
        context = {
            'student_username': user.first_name.capitalize()
        }
    except Student.DoesNotExist:
        context = None

    return render(request, 'course/home/home.html', context)

#logout
def logout_view(request):
    logout(request)
    request.session.flush() 
    return redirect('login')

# login & register view

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Fetch the student user
            student = Student.objects.get(username=username)
            
            # Validate the password
            if check_password(password, student.password):
                request.session['student_user'] = student.username
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password")
    
    return render(request, "course/registration/login.html")

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            student = Student(
                username = form.cleaned_data['username'],
                email = form.cleaned_data['email'],
                password = make_password(form.cleaned_data['password']),  
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name'],
                phone = form.cleaned_data['phone']  
            )
            student.save()
            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'course/registration/register.html', {'form': form})

# course View
def course(request):
    student_username = request.session.get('student_user', None)
    courses = Course.objects.all().order_by('id')
    if not student_username:
        return render(request, 'course/home/home.html', {"courses":courses})
    try:
        user = Student.objects.get(username=student_username)
        context = {
            "courses":courses,
            'student_username': user.first_name.capitalize()
        }
    except Student.DoesNotExist:
        context = None
    return render(request,'course/home/course.html',context)

# course About
def courseAbout(request,course_id):
    
    course = Course.objects.filter(id = course_id).first()
    if course:
        technologies = course.technology_used.split(",") if course.technology_used else []
        skills = course.course_skills.split(",") if course.course_skills else []
        return render(request,'course/home/courseAbout.html',{"course":course,'active_page': 'course','technologies':technologies,'skills':skills})
    else:
        messages.warning(request,"No such course found")
        return redirect('courses')


#course Details

def courseDetails(request):
    
    return render(request,'course/home/courseDetails.html',{'active_page': 'course'})



def courseEnroll(request,course_id):
    course = Course.objects.filter(id= course_id).first()
    
    return render(request , 'course/home/courseEnroll.html',{"course":course})




# live link view


def live(request):
    return render(request,)

#profile view

def profile(request):
    return render(request,'course/home/profile.html')


#Notification View

def notifications(request):
    return render(request,'course/home/notifications.html')