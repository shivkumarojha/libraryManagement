from django.shortcuts import render, HttpResponse, render
from django.views.decorators.csrf import csrf_protect
from .decorators import admin_user_required, staff_user_required, student_user_required
from django.contrib import messages
from .forms import UserForm, StudentProfileForm, ClassNameForm, SectionForm, AddBookForm, IssueForm, ChangePasswordForm
from django.shortcuts import redirect
from registration.models import User, StudentProfile, ClassName, Section
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Book, Issue
from datetime import timedelta, datetime
from django.http import JsonResponse
from django.core import serializers

@csrf_protect   
@admin_user_required
def adminDashboard(request):
    noOfStudents = StudentProfile.objects.count()
    noOfBooks = Book.objects.count()
    noOfIssuedBooks = Issue.objects.count()
    context = {
        'noOfStudents': noOfStudents,
        'noOfBooks': noOfBooks,
        'noOfIssuedBooks': noOfIssuedBooks
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


# View Student
@admin_user_required
def viewStudents(request):
    students = StudentProfile.objects.all()
    noOfStudents = StudentProfile.objects.count()
    if request.method == 'POST':
        searchText = request.POST.get('searchInput')
        filterStudentsByEmail = StudentProfile.objects.filter(user__email__icontains=searchText)
        filterStudentsByName = StudentProfile.objects.filter(user__fullName__icontains=searchText)
        filteredStudents = filterStudentsByName | filterStudentsByEmail
        context = {
            'students': filteredStudents
        }        
        return render(request, 'library/admin/viewStudents.html', context )
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

# delete Student
@admin_user_required
def deleteStudent(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()        
        messages.success(request, "Successfully deleted Student- "+ str(user.fullName))
        return redirect(request.META.get('HTTP_REFERER'))


# Class section Start

# Add Class
@admin_user_required
def addClass(request):
    if request.method == 'POST':
        form = ClassNameForm(request.POST)
        if form.is_valid():
            className = form.cleaned_data['className']
            form.save()
            messages.success(request, className + " class added Successfully")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = ClassNameForm

    context = {
        'form': form
    }
    return render(request, 'library/admin/addClass.html', context)


# Add Section
@admin_user_required
def addSection(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            className = form.cleaned_data['className']
            section = form.cleaned_data['section']
            form.save()
            messages.success(request, str(className) +" section - " + str(section) + "  added Successfully")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = SectionForm

    context = {
        'form': form
    }
    return render(request, 'library/admin/addSection.html', context)


# View Classes
@admin_user_required
def viewClasses(request):
    # Search Method implemented
    if request.method == 'POST':
        searchText = request.POST.get('searchInput')
        className = ClassName.objects.filter(className__icontains=searchText)
        sections = Section.objects.all()

        context = {
            'className': className,
            'sections': sections
        }        
        return render(request, 'library/admin/viewClasses.html', context )


    className = ClassName.objects.all().order_by('className')
    sections = Section.objects.all()
    context = {
        'className': className,
        'sections': sections
    }
    return render(request, 'library/admin/viewClasses.html', context)


# Edit Class Name
@admin_user_required
def updateClassName(request, pk):
    className = ClassName.objects.get(id=pk)
    form = ClassNameForm(instance=className)
    
    if request.method == 'POST':
        form = ClassNameForm(request.POST, instance=className)
        if form.is_valid():
            form.save()
            messages.success(request, 'ClassName updated successfully')
            return redirect(reverse('library:viewClasses'))
    
    context = {
        'form': form
    }
    
    return render(request, 'library/admin/updateClassName.html', context)

@admin_user_required
def deleteClassName(request, pk):
    className = ClassName.objects.get(id=pk)
    if request.method == 'POST':
        className.delete()
        messages.success(request, 'Class Deleted Successfully')
        return redirect(reverse('library:viewClasses'))
        
    
@admin_user_required
def updateSection(request, pk):
    section = Section.objects.get(id=pk)
    form = SectionForm(instance=section)
    
    if request.method ==  'POST':
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section is updated Successfully')
            return redirect(reverse('library:viewClasses'))
    
    context = {
        'form': form
    }
    
    return render(request, 'library/admin/updateSection.html', context)

# For Delete Section
@admin_user_required
def deleteSection(request, pk):
    section = Section.objects.get(id=pk)
    
    if request.method == 'POST':
        section.delete()
        messages.success(request, 'Section is deleted successfully')
        return redirect(reverse('library:viewClasses'))


# Add Book
@admin_user_required
def addBook(request):
    form = AddBookForm
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            bookName = form.cleaned_data['bookName']
            quantity = form.cleaned_data['quantity']
            book = form.save(commit=False)
            book.stock = quantity
            book.save()
            messages.success(request, 'Book ' + bookName + ' added Successfully')
            return redirect(request.META.get('HTTP_REFERER'))
    context = {
        'form': form
    }
    return render(request, 'library/admin/addBook.html', context)

# View Books
@admin_user_required
def viewBooks(request):
    if request.method == 'POST':
        searchText = request.POST.get('searchInput')
        books = Book.objects.filter(bookName__icontains=searchText)
        context = {
            'books': books
        }        
        return render(request, 'library/admin/viewBooks.html', context )
    books = Book.objects.all()
    countOfBooks = Book.objects.count()
    context = {
        'books': books,
        'countOfBooks': countOfBooks
    }
    return render(request,'library/admin/viewBooks.html', context)



# Update Book
@admin_user_required
def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    form = AddBookForm(instance=book)
    if request.method == 'POST':
        form = AddBookForm(request.POST, instance=book)
        if form.is_valid():
            # accessing previous data of form to access stock value
            prev_data = Book.objects.get(pk=form.instance.pk)
            bookName = form.cleaned_data['bookName']
            quantity = form.cleaned_data['quantity']
            book = form.save(commit=False)
            # Check the difference in quantity while updating
            difference = book.quantity - prev_data.quantity
            # Calculate updated stock
            book.stock = prev_data.stock + difference
            book.save()
            messages.success(request, 'Book ' + bookName + ' updated successfully' )
            return redirect(reverse('library:viewBooks'))
    context = {
        'form': form
    }
    return render(request, 'library/admin/updateBook.html', context)


# Delete book
@admin_user_required
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    
    
# Issue Book related views
# issue book
@admin_user_required
def issueBook(request):
    form = IssueForm
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            book = form.cleaned_data['book']

            # check stock of book
            checkBookStock = Book.objects.get(id=book.id)
            if checkBookStock.stock == 0:
                messages.info(request, 'Requested Book is not in the stock')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                # check if book is previously issued
                prevIssuedBook = Issue.objects.filter(user=user)

                # Check if student has been issued this book before
                prevBookFlag = False
                for id in prevIssuedBook:
                    if id.book_id == book.id:
                        prevBookFlag = True
                            
                if prevBookFlag:
                    messages.info(request, 'Can\'t issue one more, This book ' +str(book) + 'is previously issued')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    book = form.save()
                    # getting book from database
                    issuedBook = Issue.objects.get(id=book.id)
                    book = Book.objects.get(id=issuedBook.book_id)
                    # Fetching issued date 
                    issued_date = issuedBook.issued_date
                    # Fetching expected Date of return
                    expected_date_of_return = issued_date + timedelta(days=15)
                    # Calculating expected date of return    
                    issuedBook.expected_date_of_return = expected_date_of_return
                    # Finally Saving data into database
                    book.stock = book.stock - 1
                    book.save()
                    issuedBook.save()
                    
                    messages.success(request, str(book) + ' issued successfully')
                    return redirect(request.META.get('HTTP_REFERER'))
        
    context = {
        'form': form
    }
    
    return render(request, 'library/admin/issueBook.html', context)

# Fetch section
@admin_user_required
def fetchSection(request):
    classId = request.headers.get('classId')
    section = Section.objects.filter(className_id=classId)
    return render(request, 'library/fetchSection.html', {'section': section})
    
# Return Book 
@admin_user_required
def returnBook(request):
    form = IssueForm
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid(): 
            user = form.cleaned_data['user']
            book = form.cleaned_data['book']
            fine = 0
            issuedBook = Issue.objects.get(book_id=book.id, user=user.id)
            bookStock = Book.objects.get(id=book.id)

            if issuedBook.book.id == book.id:
                if issuedBook.returned == False:
                    issuedBook.returned = True
                    issuedBook.date_of_return = datetime.now()
                    
                    # Calcuating extra days after expected date of return
                    extraDays = datetime.now() - issuedBook.expected_date_of_return
                    extra = extraDays.days
                    
                    # Calculating fine
                    if extra > 0:
                        fine = extra * 15
                        issuedBook.fine = 15 * extra
                    issuedBook.save()
                    # increase the stock after collecting book from student
                    bookStock.stock = bookStock.stock + 1
                    bookStock.save()
                    messages.success(request, 'Book returned successfully and fine is ' + str(fine) )
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    messages.info(request, 'Book has been returned previously')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.info(request, str(book) + 'has not been issued to student' + str(user))
        
    context = {
        'form': form
    }
    return render(request, 'library/admin/returnBook.html', context)

# Fetch books for return 
@admin_user_required
def filterBooks(request):
    userId = request.headers.get('userId')
    books = Issue.objects.filter(user_id=userId,returned=False)
    context = {
     'books': books   
    }
    return render(request, 'library/admin/filterBooks.html', context)


# manage issued books
@admin_user_required
def manageIssuedBooks(request):
    
    # Search Impletation
    if request.method == 'POST':
        searchText = request.POST.get('searchInput')
        filterByIssuedBooks = Issue.objects.filter(book__bookName__icontains=searchText)
        filterByIssuedBookUserEmail = Issue.objects.filter(user__email__icontains=searchText)
        filterByIssuedBookReturned = Issue.objects.filter(returned__icontains=searchText)
        print(filterByIssuedBookReturned)
        issuedBooks = filterByIssuedBooks|filterByIssuedBookUserEmail|filterByIssuedBookReturned
        context = {
            'issuedBooks': issuedBooks,
        }        
        return render(request, 'library/admin/manageIssuedBooks.html', context )

    issuedBooks = Issue.objects.all()
    countOfIssuedBooks = Issue.objects.count()
    context = {
        'issuedBooks': issuedBooks,
        'countOfIssuedBooks': countOfIssuedBooks
    }
    return render(request, 'library/admin/manageIssuedBooks.html', context)



# Delete Issued Book
@admin_user_required
def deleteIssuedBook(request, pk):
    issuedBook = Issue.objects.get(id=pk)
    if request.method == 'POST':
        if issuedBook.returned ==  False:
            # changing the stock
            bookStock = Book.objects.get(id=issuedBook.book_id)
            bookStock.stock = bookStock.stock + 1
            bookStock.save()
        issuedBook.delete()
        messages.success(request, 'Book deleted successfully')
        return redirect(request.META.get('HTTP_REFERER'))

# View Book by class Name 
@admin_user_required
def viewBookByClassName(request, pk):
    
    books = Book.objects.filter(className=pk)
    countOfBooks = books.count()
    
    # Search Method
    if request.method == 'POST':
        searchText = request.POST.get('searchInput')
        books = books.filter(bookName__icontains=searchText)
        context = {
            'books': books
        }        
        return render(request, 'library/admin/viewBooks.html', context )
    
    context = {
        'books': books,
        'countOfBooks': countOfBooks
    }
    return render(request, 'library/admin/viewBooks.html', context)

# change Admin Password
@admin_user_required
def changeAdminPassword(request, pk):
    user = User.objects.get(id=pk)
    form = ChangePasswordForm(instance=user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Password Changed!")
            return redirect(request.META.get('HTTP_REFERER'))
    
    context = {
        'form': form
    }
    return render(request, 'library/admin/changeAdminPassword.html', context)