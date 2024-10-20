from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,'course/home/home.html')
def course(request):
    return render(request,'course/home/course.html')

def courseDetails(request):
    context = {'active_page': 'course'}
    return render(request,'course/home/courseDetails.html',context)
def live(request):
    return render(request,)

def profile(request):
    return render(request,'course/home/profile.html')
def notifications(request):
    return render(request,'course/home/notifications.html')