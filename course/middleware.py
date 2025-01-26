
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
            '/validate-email/',
            '/forgot-password/'
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
