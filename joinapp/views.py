from subprocess import SubprocessError
from django.contrib import messages
from django.forms import PasswordInput
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
def login(request):
    if request.method=="POST":
        username=request.POST=['username']
        password=request.POST=['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('/')
    else:
        return render(request,'login.html')
def joinus(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('joinus')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('joinus')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email)
                user.save()
                messages.info(request,'user created')
                return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('joinus')
        return redirect('/')
    else:
        return render(request,'joinus.html')

