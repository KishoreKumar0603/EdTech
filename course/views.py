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

#userName Validation
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def validate_username(request):
    username = request.GET.get('username', None)
    if username is None:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    data = {
        'is_taken': Student.objects.filter(username=username).exists()
    }
    return JsonResponse(data)



# Registration view

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user after validation
            student = Student(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone']
            )
            student.save()
            messages.success(request, "Registration successful!")  # Success message
            return redirect('login')
        else:
            # Form is invalid; capture form errors and display them
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
        return render(request, 'course/home/home.html', context=None)
    try:
        user = Student.objects.get(username=student_username)
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)

        # Query notifications based on time categories
        today_notifications = Notification.objects.filter(created_at__gte=today_start)
        yesterday_notifications = Notification.objects.filter(created_at__gte=yesterday_start, created_at__lt=today_start)
        earlier_notifications = Notification.objects.filter(created_at__lt=yesterday_start)

        context = {
            'student_username': user.first_name.capitalize(),
            'today_notifications': today_notifications,
            'yesterday_notifications': yesterday_notifications,
            'earlier_notifications': earlier_notifications,
        }  
    except Student.DoesNotExist:
        context = None

    return render(request, 'course/home/home.html', context)


# course View

def course(request):
    student_username = request.session.get('student_user', None)
    courses = Course.objects.all().order_by('id')
    context = {'courses': courses}
    
    if student_username:
        try:
            user = Student.objects.get(username=student_username)
            user_enrolled_course = user.enrollments.all()
            context.update({
                "courses":courses,
                'student_username': user.first_name.capitalize(),
                'enrolled_coures':user_enrolled_course
            })
        
        except Student.DoesNotExist:
            pass
    return render(request,'course/home/course.html',context)


# course About
def course_about(request,course_id):
    
    course = Course.objects.filter(id = course_id).first()
    checkpoints = course.checkpoint_set.all()
    if course:
        skills = course.get_skill_list()  
        checkpoints = Checkpoint.objects.filter(course=course)
        
        #split the technology user string to list for rendering as badge in html
        for checkpoint in checkpoints:
            checkpoint.technology_list = checkpoint.technology_used.split(",")
        context = {
            'active_page': 'course',
            'course': course,
            'skills': skills,
            'checkpoints': checkpoints
        }
        return render(request,'course/home/courseAbout.html',context)
    else:
        messages.warning(request,"No such course found")
        return redirect('courses')


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    checkpoints = Checkpoint.objects.filter(course=course)  # Retrieve all checkpoints
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

def course_enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # get the authenticated student
    student_username = request.session.get('student_user')
    student = get_object_or_404(Student, username=student_username)

    # Pre-fill the form with student data
    initial_data = {
        'name': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'phone': student.phone,
    }

    if request.method == 'POST':
        
        if Enrollment.objects.filter(student=student, course=course).exists():
            messages.info(request, "You are already enrolled in this course.")
            return redirect('course_detail', course_id=course_id)
        
        Enrollment.objects.create(student=student, course=course)
        messages.success(request, "You have been successfully enrolled in the course!")
        return redirect('course_detail', course_id=course_id)

    context = {
        'course': course,
        'initial_data': initial_data,
    }
    return render(request, 'course/home/courseEnroll.html', context)




# live link view

def live(request):
    return render(request,)



#profile view

def profile_view(request):
    student_username = request.session.get('student_user')
    student = get_object_or_404(Student, username=student_username)
    
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.profile_picture = request.FILES.get('profile_picture') or student.profile_picture

        student.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    context = {
        'student': student,
    }
    return render(request, 'course/home/profile.html', context)



#Notification View

def notifications(request):
    return render(request,'course/home/notifications.html')

def notifications_view(request):
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)

    # Query notifications based on time categories
    today_notifications = Notification.objects.filter(created_at__gte=today_start)
    yesterday_notifications = Notification.objects.filter(created_at__gte=yesterday_start, created_at__lt=today_start)
    earlier_notifications = Notification.objects.filter(created_at__lt=yesterday_start)

    context = {
        'today_notifications': today_notifications,
        'yesterday_notifications': yesterday_notifications,
        'earlier_notifications': earlier_notifications,
    }
    return render(request, 'course/home/notifications.html', context)