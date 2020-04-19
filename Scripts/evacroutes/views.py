from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from ussd.models import Victim, Volunteer
from ussd.utilities.SMS import SMS
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import Update

# Create your views here.
@csrf_exempt
def index(request):
    if request.method=='POST':
        phone=request.POST.get('phone_number')
        victim=list(Victim.objects.filter(phone_number=phone))[0]
        victim.setRescued(True)
        victim.save()
    victims = Victim.objects.all().order_by('reported_date')
    return render(request, 'evacroutes/map.html', {'victims':list(victims)})

def home(request):
    return render(request, 'evacroutes/home.html')
@csrf_exempt
def form(request):
    if request.method == 'POST':
        print("HEllo")
        u = request.POST.get('update')
        update = Update(message = u)
        update.save()
        victims=Victim.objects.all()
        recipients=["+"+str(victim.phone_number) for victim in list(victims)]
        recipients.extend(["+"+str(volunteer.phone_number) for volunteer in list(Volunteer.objects.all())])
        message="Update on Disaster\n"
        message+=u
        SMS().send_sms_sync(recipients=recipients,message=message)
        return redirect("/")
    return render(request, 'evacroutes/form.html')

def about(request):
    return render(request, 'evacroutes/about.html')


def data(request):
    victims = []
    victims = Victim.objects.all()
    return render(request, 'evacroutes/display.html', {'victims': victims})