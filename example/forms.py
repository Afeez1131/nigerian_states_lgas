from django import forms
from example.models import About
# from src.forms import StateForm, LocalGovernmentForm
from nigerian_states.fields import StateFormField, LocalGovernmentField
from nigerian_states.enums import PoliticalZones


class AboutForm(forms.ModelForm):
    state = StateFormField(
            label='Name of States',
            help_text='Select a state from the dropdown',
            zones=[PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_EAST],
            widget=forms.Select(attrs={'class': 'select form-select select2', 'required': 'required'}),
    )
    lga = LocalGovernmentField(label='Local Governments',
                                help_text='Select a LGA from the dropdown', 
                                zones=[PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_EAST],
                                widget=forms.Select(attrs={'class': 'select form-select select2', 'required': 'required'}))
    
    class Meta:
        model = About
        fields = ['name', 'state', 'lga']