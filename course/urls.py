from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('course/',views.course,name='courses'),
    path('course/course-my-progress/<slug:course_slug>/', views.course_details, name='course_detail'),
    path('profile/',views.profile_view,name="profile"),


    #login & register
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot-password/',views.forgot_password, name='forgot_password'),


    path('course/course-detail/<slug:course_slug>/', views.course_about, name='course_about'),
    path('enroll/<slug:course_slug>/', views.course_enroll, name='enroll'),
    path('unenroll/<str:course_slug>/', views.unenroll_course, name='unenroll_course'),
    path('notification/',views.notifications_view,name='notification'),
    
    #Form validation
    path('validate-username/', views.validate_username, name='validate_username'),
    path('validate-email/', views.validate_userEmail, name='validate_email'),
    
    
    #progress bar
    # path('progress-chart/<str:username>/', views.student_progress_chart, name='student_progress_chart'),

]
