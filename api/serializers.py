from rest_framework import serializers
from flightres.models import Report, FlightPermission
from registry.models import SheetRegister


class FlightRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightPermission
        fields = '__all__'


class WhatsappComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class SheetRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SheetRegister
        fields = '__all__'
