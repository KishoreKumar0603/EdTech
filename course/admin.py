from django.contrib import admin
from .models import Student, Domain, Course, Checkpoint, Enrollment,Notification
from .admin_form import *
import time
from django.core.exceptions import ObjectDoesNotExist
from supabase import create_client
from dotenv import load_dotenv
import os
# Inline admin for Checkpoints with StackedInline for vertical layout
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

    def delete_old_file_from_supabase(self, bucket_name, old_file_url):
        try:
            # Extract the file path from the full URL
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
        # Check if there is a new file being uploaded for the thumbnail
        uploaded_file = request.FILES.get("course_thumbnail_file")
        
        if uploaded_file:
            file_content = uploaded_file.read()
            timestamp = int(time.time())
            file_name = f"{obj.course_title}_{timestamp}.jpg"

            # If it's an update (change is True) and there's an old thumbnail, delete it from Supabase
            if change and obj.course_thumbnail:
                print("changing....")
                self.delete_old_file_from_supabase('courseThumbnails', obj.course_thumbnail)

            # Upload the new thumbnail to Supabase
            try:
                response = supabase.storage.from_("courseThumbnails").upload(file_name, file_content)
                print(f"Upload response: {response}")
                
                if hasattr(response, 'path') and response.path:
                    obj.course_thumbnail = supabase.storage.from_("courseThumbnails").get_public_url(file_name)
                    print(f"New thumbnail uploaded successfully: {obj.course_thumbnail}")
            except Exception as e:
                raise Exception(f"Failed to upload thumbnail: {e}")

        # Always call the superclass save_model to save the object in the database
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Before deleting the object, check if there is a course thumbnail and delete it from Supabase
        print("delete_model is called")
        if obj.course_thumbnail:
            print("deleting the old image")
            self.delete_old_file_from_supabase('courseThumbnails', obj.course_thumbnail)

        # Proceed with the usual deletion of the course model
        super().delete_model(request, obj)


# def save_model(self, request, obj, form, change):
#     uploaded_file = request.FILES.get("course_thumbnail_file")
#     if uploaded_file:
#         file_content = uploaded_file.read()
#         timestamp = int(time.time())
#         file_name = f"{obj.course_title}_{timestamp}.jpg"

#         # Upload to Supabase
#         try:
#             response = supabase.storage.from_("courseThumbnails").upload(file_name, file_content)
#             print(response)

#         except Exception as e:
#             raise Exception(f"Failed to upload thumbnail: {e}")
#         obj.course_thumbnail = supabase.storage.from_("courseThumbnails").get_public_url(file_name)

#     super().save_model(request, obj, form, change)

    

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
