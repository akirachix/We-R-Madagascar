from django.forms import ModelForm
from registry.models import Aircraft, Operator


class AircraftForm(ModelForm):
    class Meta:
        model = Aircraft
        fields = '__all__'


class OperatorForm(ModelForm):
    class Meta:
        model = Operator
        fields = '__all__'
