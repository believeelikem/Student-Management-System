from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm,LoginForm
from django.contrib.auth import login,logout,authenticate


def home(request):
    return render(request,"home.html")

def register(request):
    form = CustomUserCreationForm()
    # print(form["role"])
    # print(vars(form))
    
    if request.method == "POST":
        form = CustomUserCreationForm(data = request.POST)
        if form.is_valid():
            user =form.save(commit = False)
            user.role = "student"
            user.save()
    context = {
        "form":form
    }
    return render(request,"users/register.html",context)

def login_view(request):
    if request.user.is_authenticated:
        role = request.user.role
        return redirect(f"main:{role}_dashboard")
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        
        if form.is_valid():
            school_id = form.cleaned_data.get("school_id")
            password = form.cleaned_data.get("password")
            print(vars(form))
            print("The username is")
                                
            user = authenticate(request, school_id = school_id, password = password)
            
            if user is not None:
                login(request,user)
                if user.role == "student":
                    return redirect("main:student_dashboard")
                elif user.role == "admin":
                    return redirect("main:admin_dashboard")
                elif user.role == "teacher":
                    return redirect("main:teacher_dashboard")                
            
    return render(request,"users/login.html",{"form":form})


def logout_view(request):
    print("called")
    logout(request)
    return redirect("users:home")

def profile(request):
    return render(request,"users/profile.html")
def profile_update(request,username):
    return render(request,"users/profile_update.html")