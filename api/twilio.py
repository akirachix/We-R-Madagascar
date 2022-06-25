import os
from decouple import config
import telerivet

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


@csrf_exempt
def webhook(request):
    webhook_secret = '2K2ZFHR3QDCWM46PZ6AR2NAPM6ZC7MZZ'
    if request.POST.get('secret') != webhook_secret:
        print("hey Guys")
        return HttpResponse("Invalid webhook vd dcdd secret", 'text/plain', 403)
        if request.POST.get('event') == 'incoming_message':
            content = request.POST.get('content')
            from_number = request.POST.get('from_number')
            phone_id = request.POST.get('phone_id')
            
            return HttpResponse(json.dumps({
                'messages': [
                    {'content': "Thanks for your messagessss!"}
                    ]
                    }), 'application/json')
