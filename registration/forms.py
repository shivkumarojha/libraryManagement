from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label='Enter Email', max_length=100)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    
    

class SignUpStaff(forms.Form):
    pass



class SignUpStudent(forms.Form):
    pass