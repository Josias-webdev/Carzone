from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User

# Create your views here.

def inquiry(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        car_title = request.POST['car_title']
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        customer_need = request.POST['customer_need']
        city = request.POST['city']
        state = request.POST['state']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        if request.user.is_authenticated:
            user_id = request.user.id

            has_contacted = Contact.objects.all().filter(car_id=car_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'Vous avez deja une demande en attent pour cet article. nous vous contacterons tres bientot')
                return redirect('/cars/'+car_id)
            else:

                contact = Contact(car_id=car_id, car_title=car_title, user_id=user_id, 
                first_name=first_name, last_name=last_name, customer_need=customer_need,
                city=city, state=state, email= email, phone=phone, message=message)

                # Send an email when a user make an inquiry
                admin_info = User.objects.get(is_superuser=True)
                admin_email = admin_info.email
                send_mail(
                    'Nouvelle demande de voiture', 
                    'Vous avez une nouvelle demande de voiture de la marque ' + car_title + ' connectez vous pour en savoir plus', 
                    'joejosiasb@outlook.com',
                    [admin_email], fail_silently=True
                    )

                contact.save()
                messages.success(request, 'votre message a été envoyer, nous allons vous contactez dans peu de temps')

                return redirect('/cars/' + car_id)


    return render(request, 'contact.html')