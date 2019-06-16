from .models import Flight
from django import forms
from django.forms import widgets

class FlightAdminForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['destination_from', 'destination_to', 'departure_time', 'arrival_time',
                  'flight_distance', 'connections', 'price', 'airline', 'rows_economy',
                  'cols_economy', 'rows_business', 'cols_business', 'rows_first', 'cols_first',
                  'discount', 'checked_baggage']

    def clean(self):
        cleaned_data = self.cleaned_data

        destination_from = cleaned_data.get('destination_from')
        destination_to = cleaned_data.get('destination_to')

        depature_time = cleaned_data.get('departure_time')
        arrival_time = cleaned_data.get('arrival_time')

        if depature_time is not None and arrival_time is not None:
            if depature_time > arrival_time:
                raise forms.ValidationError("Invalid departure or arrival time")

        if destination_from == destination_to:
            raise forms.ValidationError("Destinations must be different")

        return cleaned_data


class CalculateForm(forms.Form):
    date_from = forms.DateField(widget=widgets.SelectDateWidget)
    date_to = forms.DateField(widget=widgets.SelectDateWidget)
