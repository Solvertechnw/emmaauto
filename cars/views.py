from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.conf import settings
from .models import Car
from .forms import ContactForm  # ← import your ContactForm


def home(request):
    cars = Car.objects.all().order_by('-year')[:6]
    return render(request, "cars/home.html", {"cars": cars})


def car_list(request):
    cars = Car.objects.all()
    return render(request, "cars/list.html", {"cars": cars})


def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug)
    return render(request, "cars/detail.html", {"car": car})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                send_mail(
                    subject=f"Message from {name}: {subject}",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=["rheinboltjunior4@gmail.com"],
                    fail_silently=False,
                )
                messages.success(request, "✅ Message sent successfully!")
                form = ContactForm()  # clear form after sending
            except BadHeaderError:
                messages.error(request, "❌ Invalid header found.")
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, "cars/contact.html", {"form": form})
