from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .utilities.SMS import SMS
from .utilities.location import sortlocations,reversegeocode
from .models import Victim, Volunteer
from evacroutes.models import Update
import requests
import time


@csrf_exempt
def ussdrelief(request):
    s=SMS()
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""
        
        volunteer = Volunteer.objects.filter(phone_number=phone_number)
        if(volunteer):
            volunteer = list(volunteer)[0]
            victims=Victim.objects.filter(volunteer=volunteer).filter(rescued=False)
            victims = list(victims)
            if text == "":
                response = "CON What do you want to do\n"
                response += "1. List people in need\n"
                response += "2. Send an alert\n"

            elif text[0] == '1':
                textlist=text.split('*')
                idx=textlist.count('1')-textlist.count('0')-1
                print(textlist)
                if(victims):
                    if text[-1]=='5':
                        victims[idx].setRescued(True)
                        victims[idx].save()
                        response+="END Success"
                        return HttpResponse(response)
                    if idx==len(victims):
                        response+="END The list has ended\n"
                    elif idx==len(victims)-1:
                        response+="CON "
                    else:
                        response+="CON "
                    if idx!=len(victims):
                        response+=str(victims[idx].phone_number)
                        response+=" "
                        response+=victims[idx].location
                        response+="\nPress 5 to indicate victim has been rescued\n"
                        if idx!=len(victims)-1:
                            response+="Press 1 for next\n"
                        if idx!=0:
                            response+="Press 0 for back\n"
                else:
                    response+="END No nearby victim"
                

            elif text == "2":
                response = "END Send the alert via SMS to\n"
                response+="86387 as\n"
                response+="ALERT text"

        else:
            response = "END Please send the nearest\n"
            response += "landmark to 86387 via SMS\n"
            response += "along with your pincode"

        return HttpResponse(response)
    else:
        return HttpResponse("Response can't be made")

@csrf_exempt
def sms(request):
    
    s=SMS()
    if request.method == 'POST':
        fro = request.POST.get('from')
        to = request.POST.get('to')
        text = request.POST.get('text')
        date = request.POST.get('date')
        id = request.POST.get('id')
        if text[:5]!="ALERT" and text[:4]!="HELP":
            query=text.replace(' ', '%20')
            key='Aqxws6GyR0KaQH-uo9w92nqNeePHAzsbkVDbrpiayIiAwfTbXcML-wj1XLEBPQcQ'
            url='http://dev.virtualearth.net/REST/v1/Locations?q='+query+'&o=json&key='+key
            result=requests.get(url)
            result=result.json()
            lat,lon=result['resourceSets'][0]['resources'][0]['point']['coordinates']
        if to=="86386":
            victim=Victim.objects.filter(phone_number=fro)
            if(victim):
                victim=list(victim)[0]
                victim.updateLocation(lat,lon,text)
            else:
                victim=Victim(phone_number=fro,lat=lat,lon=lon,location=text,rescued=False)
            volunteer=sortlocations(victim.lat,victim.lon,list(Volunteer.objects.all()))[0]
            victim.assign(volunteer=volunteer)
            victim.save()
            recipients=["+"+str(victim.phone_number)]
            message="You have been assigned volunteer at "+volunteer.location+". His number is "+str(volunteer.phone_number)+". For help, send \"HELP message\" to 86387. To cancel request go to our ussd code *384*3833#"
            s.send_sms_sync(recipients=recipients,message=message)
        elif to=="86387" and text[:5]=="ALERT":
            volunteer=list(Volunteer.objects.filter(phone_number=fro))[0]
            victims=Victim.objects.filter(volunteer=volunteer)
            recipients=["+"+str(victim.phone_number) for victim in list(victims)]
            message=text[6:]
            message+= "\n- "+str(volunteer.phone_number)
            s.send_sms_sync(recipients=recipients,message=message)
        elif to=="86387" and text[:4]=="HELP":
            victim=list(Victim.objects.filter(phone_number=fro))[0]
            recipients=["+"+str(victim.volunteer.phone_number)]
            message=text[5:]
            message+= "\n- "+str(victim.phone_number)
            s.send_sms_sync(recipients=recipients,message=message)
        elif to=="86387":
            volunteer=Volunteer(phone_number=fro,lat=lat,lon=lon,location=text)
            for victim in list(Victim.objects.all()):
                victim.assign(sortlocations(victim.lat,victim.lon,[victim.volunteer,volunteer])[0])
                victim.save()
            volunteer.save()
        return HttpResponse("Success")

@csrf_exempt
def index(request):
    s=SMS()
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""
        
        victim = Victim.objects.filter(phone_number=phone_number)
        if(victim):
            victim=list(victim)[0]
            updates = Update.objects.order_by('time')
            updateslist = list(updates)
            if text == "":
                response = "CON What do you want to do\n"
                response += "1. Support Services\n"
                response += "2. Reach a Shelter\n"

            elif text == "1":
                victim.setRescued(False)
                victim.save()
                response += "CON Dont worry. Stay Strong\n"
                response+="Our response team will soon be there for you\n"
                response+="1.Update your Location\n"
                response += "2.Cancel request for help"

            elif text == "1*1":
                response = "END Please send the new\n"
                response += "landmark to 86386 via SMS\n"
                response += "along with your pincode"
            
            elif text == "1*2":
                victim.setRescued(True)
                victim.save()
                response += "END We are glad that you safe now\n"

            elif text[0] == "2":
                volunteers=sortlocations(victim.lat,victim.lon,list(Volunteer.objects.all()))
                textlist=text.split('*')
                idx=textlist.count('9')-textlist.count('7')
                if text[-1]=='5':
                    victim.setRescued(False)
                    victim.assign(volunteers[idx])
                    victim.save()
                    response+="END You have been assigned\n"
                    response+="volunteer at "+volunteers[idx].location+".Phone Number: "+str(volunteers[idx].phone_number)+" You can ask\n"
                    response+="for help by sending HELP message\n"
                    response+="to 86387\n"
                    return HttpResponse(response)
                else:
                    response+="CON "
                if idx!=len(volunteers):
                    response+=str(volunteers[idx].phone_number)
                    response+=" "
                    response+=volunteers[idx].location
                    if victim.volunteer.phone_number==volunteers[idx].phone_number:
                        response+="\nYou are assigned to this volunteer"
                    else:
                        response+="\nPress 5 for help or reach the shelter\n"
                    if idx!=len(volunteers)-1:
                        response+="Press 9 for next\n"
                    if idx!=0:
                        response+="Press 7 for back\n"

        else:
            response = "END Please send the nearest\n"
            response += "landmark to 86386 via SMS\n"
            response += "along with your pincode"

        return HttpResponse(response)
    else:
        return HttpResponse("Response could not be made")
@csrf_exempt
def location(request):
    if request.method == 'POST':
        s=SMS()
        phone_number = request.POST.get('phone_number')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        victim = Victim.objects.filter(phone_number=phone_number)
        location=reversegeocode(lat,lon)
        if(victim):
            victim=list(victim)[0]
            victim.updateLocation(lat=float(lat),lon=float(lon),location=location)
        else:
            victim=Victim(phone_number=phone_number, lat=float(lat),lon=float(lon),rescued=False,location=location)
        volunteer=sortlocations(victim.lat,victim.lon,list(Volunteer.objects.all()))[0]
        victim.assign(volunteer=volunteer)
        victim.save()
        recipients=["+"+str(victim.phone_number)]
        message="You have been assigned volunteer at "+volunteer.location+". His number is "+str(volunteer.phone_number)+". For help, send \"HELP message\" to 86387. Go to USSD *384*3833# to cancel request for help"
        s.send_sms_sync(recipients=recipients,message=message)
        return HttpResponse("SUCCESS")

@csrf_exempt
def locationv(request):
    if request.method == 'POST':
        s=SMS()
        phone_number = request.POST.get('phone_number')
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        volunteer = Volunteer.objects.filter(phone_number=phone_number)
        location=reversegeocode(lat,lon)
        if(volunteer):
            volunteer=list(volunteer)[0]
            volunteer.updateLocation(lat=float(lat),lon=float(lon),location=location)
            volunteer.save()
        else:
            volunteer = Volunteer(lat=float(lat),lon=float(lon),phone_number=phone_number,location=location)
            volunteer.save()
        for victim in list(Victim.objects.all()):
            victim.assign(sortlocations(victim.lat,victim.lon,[victim.volunteer,volunteer])[0])
            victim.save()
        return HttpResponse("SUCCESS")
