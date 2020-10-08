from django.forms import ModelForm
from registry.models import Aircraft


class AircraftForm(ModelForm):
    class Meta:
        model = Aircraft
        fields = '__all__'
