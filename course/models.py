from django.db import models
import os
import datetime
from django.contrib.auth.models import User

# Helper functions to generate file paths for uploads
def getFileName(request, fileName):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_fileName = "%s%s" % (now_time, fileName)
    return os.path.join('uploads/', new_fileName)

def getProfile(request, fileName):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_fileName = "%s%s" % (now_time, fileName)
    return os.path.join('users/profileImg', new_fileName)




#Student Table
class Student(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    phone = models.CharField(max_length=15)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True)
    def __str__(self):
        return f"{self.username}"

#Domain Table
class Domain(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=2000, null=False, blank=False)
    
    def __str__(self):
        return self.name


# Course Table
class Course(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    course_title = models.CharField(max_length=100, null=False, blank=False)
    course_description = models.TextField(max_length=2000, null=False, blank=False)
    course_thumbnail = models.ImageField(upload_to=getFileName, null=False, blank=False)
    course_cost = models.IntegerField(null=False,blank=False)
    course_duration = models.CharField(max_length=30, null=False, blank=False)
    course_skills = models.CharField(max_length=3000,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    lock = models.BooleanField(default=False, help_text="Tick - Locked, Untick - Unlocked")
   
    def get_technology_list(self):
           return [checkpoint.technology_used for checkpoint in self.checkpoints.all() if checkpoint.technology_used]
    def get_skill_list(self):
        return self.course_skills.split(",") if self.course_skills else []
    
    def __str__(self):
        return self.course_title
    
    
    
    
## Multiple check points for Course
class Checkpoint(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    checkpoint_title = models.CharField(max_length=255, null=False, blank=False,default="Default Checkpoint Title")
    checkpoint_description = models.TextField(null=True, blank=True, default="Default Checkpoint Description")
    checkpoint_duration = models.CharField(max_length=30, null=False, blank=False, default="1 hour")
    technology_used = models.CharField(max_length=100,null=True,blank=True, default="Not specified")
    
    def __str__(self):
        return f"{self.checkpoint_title} ({self.course.course_title})"
    
    
#Course Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    progress_percentage = models.IntegerField(default=0)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.course_title}"
    

# Notification Table
class Notification(models.Model):
    TYPE_CHOICES = [
        ('course', 'New Course'),
        ('message', 'Message'),
        ('payment', 'Payment Update'),
        ('other', 'Other')
    ]
    
    title = models.CharField(max_length=255, help_text="Title of the notification, e.g., 'New Course Available'")
    message = models.TextField(help_text="Detailed message content of the notification")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='other', help_text="Type of notification for categorization")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the notification was created")
    extra_data = models.JSONField(null=True, blank=True, help_text=" additional information like {links: , passcodes: , or metadata: }")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.title} - {self.get_type_display()}"