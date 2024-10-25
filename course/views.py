from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
# Create your views here.

#home page View
def home(request):
    return render(request,'course/home/home.html')



# login & register view
def login(request):
    return render(request,"course/login/login.html")

def register(request):
    return render(request,'course/login/register.html')


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