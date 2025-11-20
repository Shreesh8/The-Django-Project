from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from post.models import Post , ContactInfo
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        login(request,user)
        return redirect('/')
    return render(request, "account_templates/form.html", {'form':form, 'title':'Login'})

def signin_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        new_user = authenticate(username = user.username, password = password)
        login(request, new_user)
        return redirect('/')
    return render(request, "account_templates/form.html", {'form':form, 'title':'Sign in'})

def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


def admin_panel(request):

    if request.user.is_authenticated:
        name = {"name" : request.user.username}
    else:
        name = {"name" : "Guest",}

    context = {"account": name, "data_category":"default",}

    return render(request, "account_templates/admin_panel.html", context)

def admin_panel_users(request):
    users = User.objects.all()

    if request.user.is_authenticated:
        name = {"name" : request.user.username}
    else:
        name = {"name" : "Guest",}

    query = request.GET.get("q")

    if query:
        users = users.filter(
            Q(username__icontains=query)).distinct()
        

    context = {"account": name, "admin_datas":users, "data_category":"users",}

    return render(request, "account_templates/admin_panel.html", context)

def admin_panel_posts(request):
    posts = Post.objects.all()

    if request.user.is_authenticated:
        name = {"name" : request.user.username}
    else:
        name = {"name" : "Guest",}


    query = request.GET.get("q")

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(desc__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)).distinct()
        
    context = {"account": name, "admin_datas":posts, "data_category":"posts",}

    return render(request, "account_templates/admin_panel.html", context)


def admin_panel_contact(request):
    contacts = ContactInfo.objects.all()

    if request.user.is_authenticated:
        name = {"name" : request.user.username}
    else:
        name = {"name" : "Guest",}

    query = request.GET.get("q")

    if query:
        contacts = contacts.filter(
            Q(adress__icontains=query) |
            Q(email__icontains=query)|
            Q(name__icontains=query)|
            Q(surname__icontains=query)).distinct()
        
    context = {"account": name, "admin_datas":contacts, "data_category":"contacts",}

    return render(request, "account_templates/admin_panel.html", context)