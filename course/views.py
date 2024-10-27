from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from .models import *
from .forms import *

#home page View
def home(request):
    return render(request,'course/home/home.html')



# login & register view

def login(request):
    get_token(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "course/registration/login.html")

#old view of register (store data in auth_user)
# def register(request):
#     get_token(request)
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = make_password(form.cleaned_data['password'])
#             user.save()
#             messages.success(request, "Registration successful!")
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
    
#     return render(request, 'course/registration/register.html', {'form': form})

#new view for storing data in custom db
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user in auth_user table
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            # Create student profile in Student table
            Student.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            messages.success(request, "Registration successful!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'course/registration/register.html', {'form': form})



# course View
def course(request):
    courses = Course.objects.all().order_by('id')
    return render(request,'course/home/course.html',{"courses":courses})

# course About
def courseAbout(request,course_title):
    
    course = Course.objects.filter(course_title = course_title).first()
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


# live link view

def live(request):
    return render(request,)

#profile view

def profile(request):
    return render(request,'course/home/profile.html')


#Notification View

def notifications(request):
    return render(request,'course/home/notifications.html')