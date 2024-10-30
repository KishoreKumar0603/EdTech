# course/middleware.py

from django.shortcuts import redirect
from .models import Student

class StudentUserMiddleware:
    """
    Middleware to manage access based on whether the user is a student or not.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in ['/login/', '/register/', '/']:
            return None

        # Check if user is authenticated
        student_username = request.session.get('student_user')
        if student_username:
            try:
                Student.objects.get(username=student_username)
                return None 
            except Student.DoesNotExist:
                return redirect('login') 
            
            
        return redirect('login')
