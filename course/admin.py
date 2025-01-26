from django.contrib import admin
from .models import Student, Domain, Course, Checkpoint, Enrollment,Notification
from .admin_form import *
import time
from django.core.exceptions import ObjectDoesNotExist
from supabase import create_client
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO

class CheckPointInline(admin.StackedInline):
    model = Checkpoint
    extra = 1

load_dotenv()
supabase_url = os.getenv('SUPABASE_STORAGE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing")

supabase = create_client(supabase_url, supabase_key)

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    inlines = [CheckPointInline]
    list_display = ('course_title', 'domain', 'course_duration', 'course_cost', 'lock')
    search_fields = ('course_title',)

    def compress_image(self, uploaded_file, max_size=(800, 800), quality=85):
        
        try:
            image = Image.open(uploaded_file)
            image = image.convert("RGB")  

            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            output = BytesIO()
            image.save(output, format="JPEG", quality=quality)
            output.seek(0)

            return output
        except Exception as e:
            raise Exception(f"Error compressing image: {e}")

    def delete_old_file_from_supabase(self, bucket_name, old_file_url):
        try:
            file_url_without_query = old_file_url.split('?')[0]
            file_path = file_url_without_query.split(f"{supabase_url}/storage/v1/object/public/{bucket_name}/")[-1]
            
            if file_path:
                print(f"Attempting to delete file: {file_path}")
                response = supabase.storage.from_(bucket_name).remove([file_path])
                print(f"Supabase Response: {response}")
                
                if response.get("error"):
                    print(f"Error deleting old file: {response['error']}")
                else:
                    print(f"Successfully deleted old file from Supabase: {file_path}")
            else:
                print("Invalid file path. Could not extract file path from URL.")
        except Exception as e:
            print(f"Error during old file deletion: {e}")

    def save_model(self, request, obj, form, change):
        uploaded_file = request.FILES.get("course_thumbnail_file")
        
        if uploaded_file:
            compressed_file = self.compress_image(uploaded_file)
            timestamp = int(time.time())
            file_name = f"{obj.course_title}_{timestamp}.jpg"

            if change and obj.course_thumbnail:
                self.delete_old_file_from_supabase('courseThumbnails', obj.course_thumbnail)

            try:
                response = supabase.storage.from_("courseThumbnails").upload(file_name, compressed_file.getvalue())
                print(f"Upload response: {response}")
                
                if hasattr(response, 'path') and response.path:
                    obj.course_thumbnail = supabase.storage.from_("courseThumbnails").get_public_url(file_name)
                    print(f"New thumbnail uploaded successfully: {obj.course_thumbnail}")
            except Exception as e:
                raise Exception(f"Failed to upload thumbnail: {e}")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.course_thumbnail:
            print("deleting the old image")
            self.delete_old_file_from_supabase('courseThumbnails', obj.course_thumbnail)
        super().delete_model(request, obj)



class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'created_at')
    list_filter = ('type', 'created_at')  
    search_fields = ('title', 'message') 
    ordering = ('-created_at',)  
    readonly_fields = ('created_at',) 

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Student)
admin.site.register(Domain)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment)
