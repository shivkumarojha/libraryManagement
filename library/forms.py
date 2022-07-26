from django import forms
from registration.models import User, StudentProfile


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
                'placeholder': 'Enter Class Name'
            }
        )
        self.fields['section'].widget.attrs.update(
            {
                'class': 'form-control text-white bg-dark',
                'placeholder': 'Enter Section Name'
            }
        )
        