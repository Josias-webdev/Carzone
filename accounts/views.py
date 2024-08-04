from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

# Create your views here.

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'vous etes connecté')
            return redirect('dashboard')
        else:
            messages.error(request, "nom d'utilisateur ou mot de passe incorrect!")
            return redirect('signin')

    return render(request, 'accounts/signin.html')

def signup(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur existe deja!")
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Cet adresse mail existe deja')
                    return redirect('signup')
                else:
                    myuser= User.objects.create_user(first_name=firstname, last_name=lastname ,username=username, email=email, password=password)
                    myuser.first_name = firstname
                    myuser.last_name = lastname
                    myuser.save()
                    messages.success(request, 'votre compte a été crée avec succes')
                    return redirect('signin')
        else:
            messages.error(request, 'les mots de passe ne correspondent pas')


    return render(request, 'accounts/signup.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        # messages.success(request, "Vous vous etes deconnect")
        return redirect('home')

@login_required(login_url= 'signin')
def dashboard(request):
    user_inquiries = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)

    data = {
        "inquiries": user_inquiries
    }

    return render(request, 'accounts/dashboard.html', data)


