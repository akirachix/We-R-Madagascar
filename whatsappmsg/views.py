from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse

# Create your views here.

def reply_whatsapp(request):
    response = MessagingResponse()
    # num_media = int(request.values.get("NumMedia"))
    # GOOD_BOY_URL = "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
    # if not num_media:
    #     msg = response.message("Send us an image!")
    # else:
    #     msg = response.message("Thanks for the image. Here's one for you!")
    #     msg.media(GOOD_BOY_URL)
    # print(response)
    response.message("Thanks for the image. Here's one for you!")
    return str(response)