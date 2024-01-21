from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.conf import settings

User=settings.AUTH_USER_MODEL

# Create your views here.
def register_view(request):

    if request.method=="POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user=form.save()
            username=form.cleaned_data.get("username")
            messages.success(request,f"Hey {username} account was successfully created")
            new_user=authenticate(username=form.cleaned_data['email'],
                                  password=form.cleaned_data['password1']
            )
            login(request,new_user)
            return redirect("core:index")
           
    else:
        form = UserRegisterForm()
    context={
        'form':form,
    }
    return render(request,"userauths/sign-up.html",context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f"You are already logged in")
        return redirect("core:index")
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")

        try:
            user=User.objects.get(email=email)
        except:
            messages.warning(request,f"Account with {email} doesn't exist")

        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You are logged in")
            return redirect("core:index")
        else:
            messages.warning(request,f"User does not exist.Create an account")

        context={

        }

    return render(request,"userauths/login.html")

def logout_view(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect("userauths:login")