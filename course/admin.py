from django.contrib import admin
from .models import Student, Domain, Course, Checkpoint, Enrollment

# Inline admin for Checkpoints with StackedInline for vertical layout
class CheckPointInline(admin.StackedInline):
    model = Checkpoint
    extra = 1

# Custom admin for Course with CheckPoint inline
class CourseAdmin(admin.ModelAdmin):
    inlines = [CheckPointInline]
    list_display = ('course_title', 'domain', 'course_duration', 'course_cost', 'visibility')
    search_fields = ('course_title',)

# Registering models with custom admin classes
admin.site.register(Student)
admin.site.register(Domain)
admin.site.register(Course, CourseAdmin)  # Use CourseAdmin for Course
admin.site.register(Enrollment)
