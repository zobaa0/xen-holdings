from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContactForm
from .models import Testimony
from dashboard.models import Plan

# Create your views here.


def index(request):
    testimony = Testimony.objects.all()
    return render(request, 'main/index.html', {'testimonies': testimony})


def outlook(request):
    return render(request, 'main/outlook.html')


def forecast(request):
    return render(request, 'main/forecast.html')


def perspective(request):
    return render(request, 'main/perspective.html')


def strategies(request):
    return render(request, 'main/strategies.html')


def diversity(request):
    return render(request, 'main/diversity.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.send()

            messages.success(request, ('Thank you for contacting us. Our team will reach out to you soon.'))
            return redirect('main:contact')

    else:
        form = ContactForm()
        
    context = {
        'form': form
    }
    return render(request, 'main/contact_us.html', context)


def ai(request):
    return render(request, 'main/ai.html')


def forex(request):
    return render(request, 'main/forex.html')


def esg(request):
    return render(request, 'main/esg.html')


def investment(request):
    plan = Plan.objects.all()
    return render(request, 'main/investment.html', {'investments': plan})
