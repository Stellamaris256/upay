from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Client

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        elif User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('dashboard')
    return render(request, 'signup.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    logged_in_user : User = request.user
    if logged_in_user.is_superuser or logged_in_user.is_staff :
        # this returns admin to him or her own portal
        return redirect("/admin")
    
    # we write our code to either retrieve the client or create a client
    # try :
    #     client= Client.object.get(user = logged_in_user)
    #     print(client)
    # except Exception as e :
    #     print(e)
    client, existed_before = Client.objects.get_or_create(user= logged_in_user)
    print(f'Client exited before {existed_before}')
    return render(request, 'dashboard.html', {'client': client})


@login_required(login_url='login')
def transfer(request):
    return render(request, 'transfer.html')


@login_required(login_url='login')
def transactions(request):
    return render(request, 'transactions.html', {'transactions': []})


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='login')
def set_pin(request):
    return render(request, 'set_pin.html')
