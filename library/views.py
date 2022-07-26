from django.shortcuts import render, HttpResponse, render
from django.views.decorators.csrf import csrf_protect
from .decorators import admin_user_required, staff_user_required, student_user_required
from django.contrib import messages
from .forms import UserForm, StudentProfileForm
from django.shortcuts import redirect
from registration.models import User, StudentProfile
from django.urls import reverse
from django.urls import reverse_lazy
@csrf_protect   
@admin_user_required
def adminDashboard(request):
    noOfStudents = StudentProfile.objects.count()
    context = {
        'noOfStudents': noOfStudents
    }
    return render(request, 'library/adminDashboard.html', context)


@csrf_protect
@staff_user_required
def staffDashboard(request):
    return render(request, 'library/staffDashboard.html')



@csrf_protect
@student_user_required
def studentDashboard(request):
    return render(request, 'library/studentDashboard.html')

@admin_user_required
def addStudent(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        studentForm = StudentProfileForm(request.POST)
        
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save(commit=False)
            user.active = True
            user.student = True
            user.save()
            
            student = studentForm.save(commit=False)
            student.user = user
            studentForm.save()
            messages.success(request, "Student Added Successfully:-  " + str(user))
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        userForm = UserForm
        studentForm = StudentProfileForm
    
    context = {'userForm': userForm,
               'studentForm': studentForm}
    return render(request, 'library/admin/addStudent.html', context)


@admin_user_required
def viewStudents(request):
    students = StudentProfile.objects.all()
    noOfStudents = StudentProfile.objects.count()
    context = {
        'students': students,
        'noOfStudents': noOfStudents
    }
    
    return render(request, 'library/admin/viewStudents.html', context)

# Update Student
@admin_user_required
def updateStudent(request, pk):
    user = User.objects.get(id=pk)
    student = StudentProfile.objects.get(user_id=user)
    userForm = UserForm(instance=user)
    studentForm = StudentProfileForm(instance=student)
    if request.method == 'POST':
        updatedUser = UserForm(request.POST, instance=user)
        updatedStudent = StudentProfileForm(request.POST, instance=student)
        if updatedUser.is_valid() and updatedStudent.is_valid():
            updatedUser.save()
            updatedStudent.save()
            messages.success(request, "Successfully Updated Student:- " + str(user))
            return redirect(reverse('library:viewStudents'))
        
    context = {
        'userForm': userForm,
        'studentForm': studentForm
    }
    return render(request, 'library/admin/updateStudent.html', context)
    # return redirect(request.META.get('HTTP_REFERER'))

# delete Student
@admin_user_required
def deleteStudent(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()        
        messages.success(request, "Successfully deleted Student- "+ str(user.fullName))
        return redirect(request.META.get('HTTP_REFERER'))
