from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('course',views.course,name='courses'),
    path('course/courseDetails/',views.courseDetails,name='courseDetails'),
    path('profile',views.profile,name="profile"),
    path('notification',views.notifications,name='notifications'),
]
