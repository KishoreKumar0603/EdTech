# # course/middleware.py

# from django.shortcuts import redirect
# from django.urls import reverse
# from .models import Student

# class StudentUserMiddleware:
#     """
#     Middleware to manage access based on whether the user is a student or not,
#     and to allow admin access without student authentication.
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         return self.get_response(request)

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         # Skip checks for admin URLs and specified paths
#         if request.path.startswith(reverse('admin:index')) or request.path in ['/login/', '/register/', '/']:
#             return None

#         # Check if the user is authenticated as a student
#         student_username = request.session.get('student_user')
#         if student_username:
#             try:
#                 # Verify if the student exists
#                 Student.objects.get(username=student_username)
#                 return None  # Allow access if authenticated as a student
#             except Student.DoesNotExist:
#                 return redirect('login')  # Redirect if student record is not found

#         # Redirect to login if not authenticated as a student
#         return redirect('login')






from django.shortcuts import redirect
from django.urls import reverse
from .models import Student

class StudentUserMiddleware:
    """
    Middleware to manage access based on whether the user is a student or not,
    and to allow admin access without student authentication.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip checks for admin URLs and specified paths
        excluded_paths = [
            reverse('admin:index'),
            '/login/',
            '/register/',
            '/',
            '/validate-username/',
            '/validate-email/'
        ]
        if request.path in excluded_paths:
            return None

        student_username = request.session.get('student_user')
        if student_username:
            try:
                Student.objects.get(username=student_username)
                return None
            except Student.DoesNotExist:
                return redirect('login') 
        return redirect('login')
