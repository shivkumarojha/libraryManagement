from django import forms
from registration.models import User, StudentProfile, ClassName, Section
from .models import Book, Issue


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'fullName']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-control bg-dark text-white',                'placeholder': 'Email'
            }
        )
        self.fields['fullName'].widget.attrs.update(
            {
                'class': 'form-control bg-dark text-white',
                'placeholder': 'Enter Full Name'

            }
        )


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['fatherName', 'contactNo', 'className', 'section']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['section'].queryset = Section.objects.none()

        self.fields['fatherName'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter Father Name'
            }
        )
        self.fields['contactNo'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter Father Name'
            }
        )
        self.fields['className'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter Class Name',
                'onchange': 'fetchSection(event)'
            }
        )
        self.fields['section'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter Section Name'
            }
        )
       
# Class Related forms

class ClassNameForm(forms.ModelForm):
    class Meta:
        model = ClassName
        fields = ['className']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['className'] .widget.attrs.update(
            {
                'class': 'form-control bg-dark text-white',
                'placeholder': 'Enter ClassName'
            }
        )


# Section Form


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['className', 'section']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['className'] .widget.attrs.update(
            {
                'class': 'form-control bg-dark text-white',
                'placeholder': 'Enter ClassName'
            }
        )

        self.fields['section'] .widget.attrs.update(
            {
                'class': 'form-control bg-dark text-white',
                'placeholder': 'Enter Section'
            }
        )


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['bookName', 'authorName','isbn', 'className', 'quantity', 'stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bookName'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter Book Name'
            }
        )
        self.fields['authorName'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter author Name'
            }
        )
        self.fields['isbn'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter isbn number'
            }
        )
        self.fields['className'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter Class Name'
            }
        )
        self.fields['quantity'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter quantity'
            }
        )


# Issue Book Form
class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['book', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'] .widget.attrs.update(
            {
                'class': 'form-control bg-dark text-white',
                'placeholder': 'Select Book'
            }
        )

        self.fields['user'] .widget.attrs.update(
            {
                'class': 'form-control bg-dark text-white',
                'placeholder': 'Select User',
                'onchange': 'filterBooks(event)'
            }
        )
