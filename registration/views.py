from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def index(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('library/admin')
        elif request.user.is_staff:
            return redirect('library/staff')
        elif request.user.is_student:
            return redirect('library/student')
        else:
            return redirect('thanks/')
    else:
        # Post requests for Login form
        if request.method ==  'POST':
            form = LoginForm(request.POST) # binding data to the form( bound form)
            if form.is_valid():
                email = request.POST.get('email')
                password = request.POST.get('password')
                try:
                    user  = User.objects.get(email=email)
                    status = user.is_active
                except User.DoesNotExist:
                    user = None
                    status = None
                    
                if user is not None:
                    if status == True:
                        user =  authenticate(request, email=email, password=password)
                        if user is not None:
                            if user.is_admin == True and user.is_staff == True:
                                login(request, user)
                                return redirect('library:admin')
                            elif user.is_admin == False and user.is_staff == True:
                                print('User is staff')
                        else:
                            messages.error(request, 'Password doesn\'t match')
                            redirect('home')
                    else:
                        messages.error(request, 'User is not active')
                        redirect('home')
                else:
                    messages.error(request,'User Name or Password doesn\'t match')
                    redirect('home')
        else:
            form = LoginForm()
    
    return render(request, 'registration/index.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')