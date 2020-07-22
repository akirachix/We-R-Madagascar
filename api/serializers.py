from rest_framework import serializers
from flightres.models import Report, FlightPermission, Pilots
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

class PilotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilots
        fields = '__all__'

class PilotFromFlightSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True,source="pilot_id.name")
    phone_number = serializers.CharField(read_only=True,source="pilot_id.phone_number")
    address = serializers.CharField(read_only=True,source="pilot_id.address")
    cv_url = serializers.CharField(read_only=True,source="pilot_id.cv_url")
    company = serializers.CharField(read_only=True,source="pilot_id.company")
    is_active = serializers.CharField(read_only=True,source="pilot_id.is_active")

    class Meta:
        model = FlightPermission
        fields = ('pilot_id', 'name', 'phone_number', 'address', 'cv_url', 'company', 'is_active')