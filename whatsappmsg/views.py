from django.http import HttpResponse
from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.

@csrf_exempt
@xframe_options_exempt
def reply_whatsapp(request):
    if request.method == 'POST':
        response = MessagingResponse()
        print(request.POST.get('Body'))
        msg = request.POST.get('Body')
        response.message("Thanks for asking drone registry, we will check your number {}, Please send you gps".format(msg))
        return HttpResponse(str(response))
    else:
        return HttpResponse("")