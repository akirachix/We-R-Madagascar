from rest_framework import serializers
from flightres.models import WhatsappComplain, FlightRegistry

class FlightRegistrySerializer(serializers.ModelSerializer):
    class  Meta:
        model = FlightRegistry
        fields = '__all__'

class WhatsappComplainSerializer(serializers.ModelSerializer):
    class  Meta:
        model = WhatsappComplain
        fields = '__all__'