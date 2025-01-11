from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('course/',views.course,name='courses'),
    path('course/course-my-progress/<int:course_id>',views.course_details,name='course_detail'),
    path('profile/',views.profile_view,name="profile"),


    #login & register
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/', views.logout_view, name='logout'),


    path('course/course-detail/<int:course_id>/',views.course_about,name='course_about'),
    path('enroll/<int:course_id>/',views.course_enroll,name='enroll'),
    path('notification/',views.notifications_view,name='notification'),
    
    #Form validation
    path('validate-username/', views.validate_username, name='validate_username'),
    path('validate-email/', views.validate_userEmail, name='validate_email'),
    
    
    #progress bar
    path('progress-chart/<str:username>/', views.student_progress_chart, name='student_progress_chart'),

]
