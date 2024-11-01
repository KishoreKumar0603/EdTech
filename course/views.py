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
    if course:
        technologies = course.technology_used.split(",") if course.technology_used else []
        skills = course.course_skills.split(",") if course.course_skills else []
        return render(request,'course/home/courseAbout.html',{"course":course,'active_page': 'course','technologies':technologies,'skills':skills})
    else:
        messages.warning(request,"No such course found")
        return redirect('courses')






def course_enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Retrieve the authenticated student
    student_username = request.session.get('student_user')
    student = get_object_or_404(Student, username=student_username)

    # Pre-fill the form with student data
    initial_data = {
        'name': f"{student.first_name} {student.last_name}",
        'email': student.email,
        'phone': student.phone,
    }

    if request.method == 'POST':
        # Check if the student is already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            messages.info(request, "You are already enrolled in this course.")
            return redirect('course_detail', course_id=course_id)
        
        # Create a new enrollment record
        Enrollment.objects.create(student=student, course=course)
        messages.success(request, "You have been successfully enrolled in the course!")
        return redirect('course_detail', course_id=course_id)

    context = {
        'course': course,
        'initial_data': initial_data,
    }
    return render(request, 'course/home/courseEnroll.html', context)

#Enrolled course Details

def course_details(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    if course:
        technologies = course.technology_used.split(",") if course.technology_used else []
        skills = course.course_skills.split(",") if course.course_skills else []
        context = {'active_page': 'course','course':course,'technologies':technologies,'skills':skills}
    
    return render(request,'course/home/courseDetails.html',context)



# live link view


def live(request):
    return render(request,)

#profile view

def profile(request):
    return render(request,'course/home/profile.html')


#Notification View

def notifications(request):
    return render(request,'course/home/notifications.html')