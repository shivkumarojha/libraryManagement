from django.urls import path
from . import views
from registration import views as registrationView

app_name='library'

urlpatterns = [
    path('', registrationView.index, name='signIn'),
    path('admin/',views.adminDashboard, name='admin'),
    path('staff/', views.staffDashboard, name='staff'),
    path('student/', views.studentDashboard, name='student'),
    
    # Student Related url
    path('add_student/', views.addStudent, name='addStudent'),
    path('view_students/', views.viewStudents, name='viewStudents'),
    path("update_student/<int:pk>/", views.updateStudent, name="updateStudent"),
    path('delete_student/<int:pk>/', views.deleteStudent, name="deleteStudent"),
]