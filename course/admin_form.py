from django import forms
from .models import Course
from supabase import create_client
from dotenv import load_dotenv
import os
load_dotenv()
SUPABASE_STORAGE_URL = os.getenv('SUPABASE_STORAGE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
if not SUPABASE_STORAGE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key is missing in environment variables.")

supabase = create_client(SUPABASE_STORAGE_URL, SUPABASE_KEY)

class CourseAdminForm(forms.ModelForm):
    course_thumbnail_file = forms.FileField(required=False, label="Thumbnail Image")

    class Meta:
        model = Course
        fields = "__all__"
