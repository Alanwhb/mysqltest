from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('studentInfo/<int:sid>/', views.studentInfo, name='studentInfo'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('manager/', views.manager, name='manager'),
    path('manager/classList/', views.classList, name='classList'),
    path('manager/addClass/', views.addClass, name='addClass'),
    path('manager/classStudent/<int:cid>/', views.classStudent, name='classStudent'),
    path('manager/studentList/', views.studentList, name='studentList'),
    path('manager/addStudent/', views.addStudent, name='addStudent'),
    path('manager/deleteStudent/<int:sid>/', views.deleteStudent, name='deleteStudent'),
    path('manager/updateStudent/<int:sid>/', views.updateStudent, name='updateStudent'),
    path('manager/teacherList/', views.teacherList, name='teacherList'),
    path('manager/addTeacher/', views.addTeacher, name='addTeacher'),
    path('manager/deleteTeacher/<int:tid>/', views.deleteTeacher, name='deleteTeacher'),
    path('manager/updateTeacher/<int:tid>/', views.updateTeacher, name='updateTeacher'),
    path('manager/courseList/', views.courseList, name='courseList'),
    path('manager/addCourse/', views.addCourse, name='addCourse'),
    path('manager/deleteCourse/<int:cid>/', views.deleteCourse, name='deleteCourse'),
    path('manager/updateCourse/<int:cid>/', views.updateCourse, name='updateCourse'),
]