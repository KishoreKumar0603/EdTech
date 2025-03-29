import json
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from .models import *
from .forms import *
from django.contrib.auth import logout
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
import time
from django.core.cache import cache
#logout
def logout_view(request):
    logout(request)
    request.session.flush() 
    return redirect('login')


#forgot password
def forgot_password(request):

    if request.method == 'POST':
        usernameOrEmail = request.POST.get('username')
        newPass = request.POST.get('Newpassword')
        confirmPass = request.POST.get('Confirmpassword')
        try:
            student = Student.objects.get(Q(username = usernameOrEmail) | Q(email=usernameOrEmail))
            
            if newPass == confirmPass:
                student.password =  make_password(newPass)
                student.save()
                messages.success(request,"Password Changed Successfully")
                return redirect('login')
            
        except Student.DoesNotExist:
            messages.error("UserName not found in Db")
    return render(request,'course/registration/forgotPassword.html')

#password change
def change_password(request):
    student_username = request.session.get('student_user')
    student = cache.get_or_set(
        f"student_{student_username}", 
        lambda: Student.objects.get(username=student_username), 
        timeout=3600
    )
    if request.method == 'POST':
        oldPassWord = request.POST.get('oldPass')
        newPassWord = request.POST.get('newPassword')
        confirmPassWord = request.POST.get('confirmPassword')

        if check_password(oldPassWord, student.password):
            if newPassWord == confirmPassWord:
                student.password = make_password(newPassWord)
                student.save()
                messages.success(request, "Password updated successfully!")
                return redirect('profile')
            else:
                messages.error(request, "New password and confirm password do not match.")
        else:
            messages.error(request, "Old password is incorrect.")

    return render(request, 'course/home/profile.html')

# login & register view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')      
        try:
            student = cache.get_or_set(
                f"student_{username}", 
                lambda: Student.objects.get(username=username), 
                timeout=3600
            )
            if check_password(password, student.password):
                request.session['student_user'] = student.username
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password")  
    return render(request, "course/registration/login.html")


#userName Validation
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def validate_username(request):
    username = request.GET.get('username', None)
    if username is None:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    data = {
        'is_taken': Student.objects.filter(Q(username=username) | Q(email=username)).exists()
    }
    return JsonResponse(data)

#Email Validation
@ensure_csrf_cookie
def validate_userEmail(request):
    userEmail= request.GET.get('email',None)
    if userEmail is None:
        return JsonResponse({'error':'Invalid request'},status=400)
    data = {
        'is_taken':Student.objects.filter(email=userEmail).exists()
    }
    return JsonResponse(data)

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            student = Student(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone']
            )
            student.save()
            messages.success(request, "Registration successful!") 
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserRegistrationForm()  
    return render(request, 'course/registration/register.html', {'form': form})


#Home view
def home(request):
    student_username = request.session.get('student_user', None)
    if not student_username:
        print("user name not passing")
        return render(request, 'course/home/home.html', context=None)
    try:
        user = cache.get_or_set(
                f"student_{student_username}", 
                lambda: Student.objects.get(username=student_username), 
                timeout=3600
            )
        notifications = cache.get("notifications")
        if not notifications:
            now = timezone.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            yesterday_start = today_start - timedelta(days=1)
            today_notifications = Notification.objects.filter(created_at__gte=today_start)
            yesterday_notifications = Notification.objects.filter(created_at__gte=yesterday_start, created_at__lt=today_start)
            earlier_notifications = Notification.objects.filter(created_at__lt=yesterday_start)
            context = {
                'student_username': user.first_name.capitalize(),
                'today_notifications': today_notifications,
                'yesterday_notifications': yesterday_notifications,
                'earlier_notifications': earlier_notifications,
            }  
            cache.set("notifications", context, timeout=3600)
        context ={ 
            "notification":notifications,
            'student_username': user.first_name.capitalize(),
            }
    except Student.DoesNotExist:
        context = None


    return render(request, 'course/home/home.html', context)


# course View
def course(request):
    student_username = request.session.get('student_user', None)
    courses = cache.get_or_set(
                "courses", 
                lambda: Course.objects.all().order_by('id'), 
                timeout=3600
            )      
    context = {'courses': courses}
    if student_username:
        try:
            user = cache.get_or_set(
                f"student_{student_username}", 
                lambda: Student.objects.get(username=student_username), 
                timeout=3600
            )
            user_enrolled_course = cache.get_or_set(
                f"enrolled_{student_username}", 
                lambda: user.enrollments.all(), 
                timeout=3600
            )
            context.update({
                "courses":courses,
                'student_username': user.first_name.capitalize(),
                'enrolled_coures':user_enrolled_course
            })
        
        except Student.DoesNotExist:
            pass
    return render(request,'course/home/course.html',context)


# course About
def course_about(request,course_slug):
    course = cache.get_or_set(
            f"course_{course_slug}", 
            lambda: Course.objects.filter(slug = course_slug).first(), 
            timeout=3600
        )
    checkpoints = course.checkpoint_set.all()
    if course:
        skills = course.get_skill_list()  
        checkpoints = Checkpoint.objects.filter(course=course)
        
        for checkpoint in checkpoints:
            checkpoint.technology_list = checkpoint.technology_used.split(",")
        context = {
            'active_page': 'course',
            'course': course,
            'skills': skills,
            'checkpoints': checkpoints
        }
        return render(request, 'course/home/courseAbout.html', context)
    else:
        messages.warning(request, "No such course found")
        return redirect('courses')
#course details
def course_details(request, course_slug):
    course = cache.get_or_set(
            f"course_{course_slug}", 
            lambda: Course.objects.filter(slug = course_slug).first(), 
            timeout=3600
        )
    checkpoints = Checkpoint.objects.filter(course=course) 
    for checkpoint in checkpoints:
            checkpoint.technology_list = checkpoint.technology_used.split(",")
    if course:
        skills = course.get_skill_list()
        context = {
            'active_page': 'course',
            'course': course,
            'skills': skills,
            'checkpoints': checkpoints
        }
    return render(request, 'course/home/courseDetails.html', context)




#Enrolled course Details
def course_enroll(request, course_slug):
    course = cache.get_or_set(
        f"course_{course_slug}", 
        lambda: Course.objects.filter(slug = course_slug).first(), 
        timeout=3600
    )
    student_username = request.session.get('student_user')
    student = cache.get_or_set(
            f"student_{student_username}", 
            lambda: Student.objects.get(username=student_username), 
            timeout=3600
        )
    initial_data = {
        'name': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'phone': student.phone,
    }
    if request.method == 'POST':
        
        if Enrollment.objects.filter(student=student, course=course).exists():
            messages.info(request, "You are already enrolled in this course.")
            return redirect('course_detail', course_slug=course_slug)
        
        Enrollment.objects.create(student=student, course=course)
        cache.delete(f"enrolled_{student_username}")
        messages.success(request, "You have been successfully enrolled in the course!")
        return redirect('course_detail', course_slug=course_slug)

    context = {
        'active_page': 'course',
        'course': course,
        'initial_data': initial_data,
    }
    return render(request, 'course/home/courseEnroll.html', context)



#unEnroll course 
def unenroll_course(request, course_slug):
    course = cache.get_or_set(
        f"course_{course_slug}", 
        lambda: Course.objects.filter(slug = course_slug).first(), 
        timeout=1800
    )
    print("Course : ",course.course_title)
    student_username = request.session.get('student_user')
    student = cache.get_or_set(
        f"student_{student_username}", 
        lambda: Student.objects.get(username=student_username), 
        timeout=3600
    )
    print("userName : ",student.username)
    # Check if the student is enrolled in the course
    enrollment = Enrollment.objects.filter(student=student, course=course).first()
    if enrollment:
        print("deleted successfull")
        enrollment.delete()
        cache.delete(f"student_{student_username}")
        cache.delete(f"enrolled_{student_username}")
    else:
        print("error")
        messages.error(request, "You are not enrolled in this course.")
    return redirect('course_detail', course_slug=course_slug)  




# live link view

def live(request):
    return render(request,)



#profile view
from utils.supabase_utils import upload_profile_image
def profile_view(request):
    student_username = request.session.get('student_user')
    student = cache.get_or_set(
        f"student_{student_username}", 
        lambda: Student.objects.get(username=student_username), 
        timeout=3600
    )
    
    if request.method == 'POST':
        student.username = request.POST.get('username')
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')

        if request.FILES.get('profile_picture'):
            profile_picture = request.FILES.get('profile_picture')
            student.profile_picture = upload_profile_image(profile_picture,student)

        student.save()
        cache.set(f"student_{student_username}", student, timeout=3600)
        return redirect('profile')

    context = {'student': student}
    return render(request, 'course/home/profile.html', context)



#Notification View
def notifications_view(request):
    cache_key = "notifications"
    notifications = cache.get(cache_key)

    if not notifications:

        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)
        today_notifications = list(Notification.objects.filter(created_at__gte=today_start))
        yesterday_notifications = list(Notification.objects.filter(created_at__gte=yesterday_start, created_at__lt=today_start))
        earlier_notifications = list(Notification.objects.filter(created_at__lt=yesterday_start))

        notifications = {
            'today_notifications': today_notifications,
            'yesterday_notifications': yesterday_notifications,
            'earlier_notifications': earlier_notifications,
            'active_page':"notification"
        }
        cache.set(cache_key, notifications, timeout=3600)

    context = {**notifications, 'active_page': "notification"}
    return render(request, 'course/home/notifications.html', context)
