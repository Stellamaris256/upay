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
    # we ensure that this portal is only accessible by a user not a superuser and if the user has access to this page  but has not yet been assigned as a Client we automatedly assign the logged in user as a Client
    logged_in_user : User = request.user
    if logged_in_user.is_superuser:
        return redirect('signup')
    
    try :
        # first query is a get query 
        bank_user = Client.objects.get_or_create(user=logged_in_user)
        return render(request, 'dashboard.html', {"client":bank_user[0]})
    except Exception as e :
        return render(request, '500.html', {})

@login_required(login_url='login')
def transfer(request):
    return render(request, 'transfer.html')


@login_required(login_url='login')
def transactions(request):
    transactions = [
        {
            "date": "2025-11-01",
            "type": "Deposit",
            "amount": "₦25,000",
            "status": "Successful"
        },
        {
            "date": "2025-11-02",
            "type": "Withdrawal",
            "amount": "₦5,000",
            "status": "Pending"
        },
        {
            "date": "2025-11-02",
            "type": "Transfer",
            "amount": "₦12,500",
            "status": "Failed"
        },
        {
            "date": "2025-11-03",
            "type": "Bill Payment",
            "amount": "₦2,000",
            "status": "Successful"
        },
        {
            "date": "2025-11-03",
            "type": "Deposit",
            "amount": "₦10,000",
            "status": "Successful"
        },
        {
            "date": "2025-11-03",
            "type": "Transfer",
            "amount": "₦8,750",
            "status": "Successful"
        },
        {
            "date": "2025-11-04",
            "type": "Withdrawal",
            "amount": "₦15,000",
            "status": "Failed"
        },
        {
            "date": "2025-11-04",
            "type": "Deposit",
            "amount": "₦30,000",
            "status": "Pending"
        },
        {
            "date": "2025-11-05",
            "type": "Transfer",
            "amount": "₦7,200",
            "status": "Successful"
        },
        {
            "date": "2025-11-05",
            "type": "Bill Payment",
            "amount": "₦1,500",
            "status": "Successful"
        }
    ]

    return render(request, 'transactions.html', {'transactions': transactions})


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='login')
def set_pin(request):
    logged_in_user : User = request.user
    if logged_in_user.is_superuser:
        return redirect('signup')
    bank_user,existed = Client.objects.get_or_create(user=logged_in_user)

    if not bank_user.pin:
        pin_set = False 
    else : 
        pin_set = True

    if request.method == 'POST':
        new_pin : str = request.POST.get("new_pin")
        confirm_pin = request.POST.get("new_pin_confirm")
        print(new_pin, confirm_pin)
        if not new_pin :
            error = "please provide your new pin"
            return render(request, 'set_pin.html', {"pin_set": pin_set, 'client' : bank_user, "error":error})
        if new_pin != confirm_pin :
            error = "both pin must match and must not be more than 4 digit"
            return render(request, 'set_pin.html', {"pin_set": pin_set, 'client' : bank_user, "error":error})
        if len(new_pin) != 4 or not new_pin.isdigit():
            error = "your new pin must be exactly 4 digit only"
            return render(request, 'set_pin.html', {"pin_set": pin_set, 'client' : bank_user, "error":error})
        if not pin_set :
            # this means the user have not set pin before 
            bank_user.pin = new_pin
            bank_user.save()
            pin_set = True 
            return render(request, 'set_pin.html', {"pin_set": pin_set, 'client' : bank_user, "success":"Pin Set Successfully"})
        
    return render(request, 'set_pin.html', {"pin_set": pin_set, 'client' : bank_user})
