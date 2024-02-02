from django import forms
from nigerian_states.models import State, LocalGovernment
from django.db import connection
    
    
class StateFormField(forms.ChoiceField):
    """
    A custom form field for selecting a state in Nigeria.This field extends the ChoiceField.
    Reason for using ChoiceField is `State` and `Town` are to be treated as `CharField`.

    Example usage:
    ```
    state = StateFormField(
            label='Name of States',
            help_text='Select a state from the dropdown',
            zones=[PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_EAST],
            widget=forms.Select(attrs={'class': 'select form-select select2', 'required': 'required'}),
    )
    ```
    #todo: Filtering states by Geo-political zones
            North Central - Benue, FCT, Kogi, Kwara, Nasarawa, Niger, Plateau. 
            North East - Adamawa, Bauchi, Borno, Gombe, Taraba, Yobe. 
            North West - Kaduna, Katsina, Kano, Kebbi, Sokoto, Jigawa, Zamfara. 
            South East - Abia, Anambra, Ebonyi, Enugu, Imo. 
            South South - Akwa-Ibom, Bayelsa, Cross-River, Delta, Edo, Rivers. 
            South West - Ekiti, Lagos, Osun, Ondo, Ogun, Oyo.
            
    kwargs `zones`: list of the political zones in Nigeria you want the states choices to be from.
    """
    def get_state_choices(self):
        choices = []
        table_names = connection.introspection.table_names()
        if 'nigerian_states_state' in table_names:
            qs = State.objects.all()
            geo_zones = self.zones
            if geo_zones:
                qs = qs.filter(zone__in=geo_zones)
            choices = [(state.name, state.name) for state in qs]
        return choices
    
    def __init__(self, *args, **kwargs):
        self.zones = kwargs.pop('zones', [])
        kwargs['choices'] = self.get_state_choices()
        super().__init__(*args, **kwargs)
        
        

class LocalGovernmentField(forms.ChoiceField):
    """
    A custom form field for selecting Local Government in Nigeria.

    Example usage:
    ```
    lga = LocalGovernmentField(label='Local Governments',
                                help_text='Select a LGA from the dropdown', 
                                zones=[PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_EAST],
                                widget=forms.Select(attrs={'class': 'select form-select select2', 'required': 'required'}))
    ```
    kwargs `zones`: list of the political zones in Nigeria you want the localgovernment choices to be from.
    """
    def get_lgas_choices(self):
        choices = []
        table_names = connection.introspection.table_names()
        if 'nigerian_states_localgovernment' in table_names:
            qs = LocalGovernment.objects.all()
            geo_zones = self.zones
            if geo_zones:
                qs = qs.filter(state__zone__in=geo_zones)
            choices = [(lga.name, f"{lga.state.name}: {lga.name}") for lga in qs]
        return choices
    
    def __init__(self, *args, **kwargs):
        self.zones = kwargs.pop('zones', [])
        kwargs['choices'] = self.get_lgas_choices()
        super().__init__(*args, **kwargs)