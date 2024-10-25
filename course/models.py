from django.db import models
import os
import datetime

# Helper functions to generate file paths for uploads
def getFileName(request, fileName):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_fileName = "%s%s" % (now_time, fileName)
    return os.path.join('uploads/', new_fileName)

def getProfile(request, fileName):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_fileName = "%s%s" % (now_time, fileName)
    return os.path.join('users/profileImg', new_fileName)

# Models
class User(models.Model):
    first_name = models.CharField(max_length=40, null=False, blank=False)
    last_name = models.CharField(max_length=40, null=False, blank=True)
    profile_img = models.ImageField(upload_to=getProfile, null=True, blank=True)  # Changed null=False to null=True
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Domain(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=2000, null=False, blank=False)
    
    def __str__(self):
        return self.name


class Course(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    course_title = models.CharField(max_length=100, null=False, blank=False)
    course_description = models.TextField(max_length=2000, null=False, blank=False)
    course_thumbnail = models.ImageField(upload_to=getFileName, null=False, blank=False)
    course_cost = models.IntegerField(null=False,blank=False)
    course_duration = models.CharField(max_length=30, null=False, blank=False)
    course_skills = models.CharField(max_length=3000,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.BooleanField(default=False, help_text="Tick - Locked, Untick - Unlocked")
    checkpoint_title = models.CharField(max_length=255, null=False, blank=False)
    checkpoint_description = models.TextField(null=True, blank=True)
    checkpoint_duration = models.CharField(max_length=30, null=False, blank=False)
    technology_used = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.course_title
    
class Checkpoint(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    