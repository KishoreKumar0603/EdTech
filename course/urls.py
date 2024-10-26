from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('course',views.course,name='courses'),
    path('course/course-detail/<str:course_title>',views.courseAbout,name='courseAbout'),
    path('course/course-my-progress/',views.courseDetails,name='courseDetails'),
    path('profile',views.profile,name="profile"),
    path('login/',views.login,name='login'),
    path('register/', views.register, name='register'),
]
