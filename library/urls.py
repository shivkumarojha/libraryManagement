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
    path('update_student/<int:pk>/', views.updateStudent, name="updateStudent"),
    path('delete_student/<int:pk>/', views.deleteStudent, name="deleteStudent"),
    
    # Class section Related url
    path('addClass/', views.addClass, name="addClass"),
    path('addSection/', views.addSection, name="addSection"),
    path('viewClasses/', views.viewClasses, name="viewClasses"),
    path("updateClassName/<int:pk>/", views.updateClassName , name="updateClassName"),
    path("deleteClassName/<int:pk>", views.deleteClassName, name="deleteClassName"),
    path('updateSection/<int:pk>/', views.updateSection, name='updateSection'),
    path('deleteSection/<int:pk>/', views.deleteSection, name='deleteSection'),
    path("viewBookByClassName/<int:pk>/", views.viewBookByClassName, name="viewBookByClassName"),
    
    # Book related URls
    path('addBook/', views.addBook, name='addBook'),
    path('viewBooks/', views.viewBooks, name='viewBooks'),
    path('updateBook/<int:pk>/', views.updateBook, name="updateBook"),
    path('deleteBook/<int:pk>/', views.deleteBook, name='deleteBook'),
    
    # Issue related URL
    path("issueBook/", views.issueBook, name="issueBook"),
    path("returnBook/", views.returnBook , name="returnBook"),
    path("manageIssuedBooks/", views.manageIssuedBooks , name="manageIssuedBooks"),
    path("deleteIssuedBook/<int:pk>/", views.deleteIssuedBook , name="deleteIssuedBook"),
    
    
    # fetch request
    path('fetchSection/', views.fetchSection, name='fetchSection'),
    path('filterBooks/', views.filterBooks, name='filterBooks'),
]