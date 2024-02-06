from django import forms
from example.models import About
# from src.forms import StateForm, LocalGovernmentForm
from nigerian_states.fields import GeoPoliticalZoneField, StateField, LocalGovernmentField
from nigerian_states.enums import PoliticalZones


class AboutForm(forms.ModelForm):
    zone = GeoPoliticalZoneField(
            label='Zone',
            empty_label='Select a Zone', # the default incase there is no zone in the field;
            help_text='Select a zone from the dropdown',
            widget=forms.Select(attrs={'class': 'select form-select select2'}),
    )
    state = StateField(
            label='Name of States',
            empty_label = 'Select a State',
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