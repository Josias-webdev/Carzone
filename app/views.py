from django.shortcuts import redirect, render
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Team
from cars.models import Car

# Create your views here.

def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured= True)
    all_cars = Car.objects.order_by('-created_date')
    # search_fields = Car.objects.values('model', 'city', 'year', 'body_style')
    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()

    data = {
        'teams': teams,
        'featured_cars': featured_cars,
        'all_cars': all_cars,
        # 'search_fields': search_fields,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,


    }

    return render(request, 'pages/home.html', data)

def about(request):

    teams = Team.objects.all()

    data = {
        'teams': teams,
    }

    return render(request, 'pages/about.html', data)

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        email_subject = "Vous avez un nouveau message de " + subject
        message_body = "Nom: " + name + "\nEmail: " + email + "\nObject: " + subject + "\nPhone: " + phone + "\nMessage: " + message

        admin_info = User.objects.get(is_superuser=True)
        admin_email = admin_info.email
        send_mail(
            email_subject, 
            message_body, 
            'joejosiasb@outlook.com',
            [admin_email], fail_silently=True
            )
        messages.success(request, "Merci de nous avoir contacter, Nous allons vous repondre dés que possible")
        return redirect('contact')
        
    return render(request, 'pages/contact.html')


 