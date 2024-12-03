from django.contrib import admin
from .models import Student, Domain, Course, Checkpoint, Enrollment,Notification

# Inline admin for Checkpoints with StackedInline for vertical layout
class CheckPointInline(admin.StackedInline):
    model = Checkpoint
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [CheckPointInline]
    list_display = ('course_title', 'domain', 'course_duration', 'course_cost', 'lock')
    search_fields = ('course_title',)
    

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
