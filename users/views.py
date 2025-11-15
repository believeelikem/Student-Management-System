from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm,LoginForm,CustomUserChangeForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


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
    return render(request,f"users/profile_{request.user.role}.html")

def profile_update(request,username):    
    from django.contrib.auth.hashers import check_password
    form = CustomUserChangeForm(instance = User.objects.get(username = username)) 
     
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST,request.FILES,instance = request.user)
        
        if form.is_valid():
            can_save = True
            password1 = form.cleaned_data.get("password1")  
            password2 = form.cleaned_data.get("password2")
            print(form.cleaned_data)
            
            if any([password1,password2]):
                old_password = request.user.password
                print(old_password)
                
                if all([password1,password2]):
                    print("both enterd ")
                    if check_password(password1,old_password):
                        print("Got here ")
                        request.user.set_password(password2)
                        return redirect("users:profile")

                    else:
                        print("Get here ")
                        form.add_error(None, "old passwords didnt match")
                        can_save = False
                else:
                    can_save = False
                    form.add_error(None,"You must enter both old and new passwords ")
            if can_save:
                form.save()
                return redirect("users:profile")
        else:
            print(form.errors)        
                
    context = {
        "form":form
    }
    return render(request,f"users/profile_update_{request.user.role}.html",context)