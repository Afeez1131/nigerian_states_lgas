from django import forms
from nigerian_states.models import State, LocalGovernment, GeoPoliticalZone
from django.conf import settings
from django.db import connection
    

DEFAULT_POLITICAL_ZONES = getattr(settings, 'DEFAULT_GEO_POLITICAL_ZONES', [])


class BaseField(forms.ChoiceField):
    """
    This is the base class for all the fields.
    kwargs:
        - empty_label: The first option in the dropdown
        - zones: Geo-Political Zones you want the fields choices to be limited to. 
          This would override the `settings.DEFAULT_GEO_POLITICAL_ZONES` 
    """
    def __init__(self, *args, **kwargs):
        self.empty_label = kwargs.pop('empty_label', None)
        self.zones = kwargs.pop('zones', [])
        kwargs['choices'] = self.get_choices()
        return super().__init__(*args, **kwargs)
    
    def geo_political_zones(self):
        geo_zones = DEFAULT_POLITICAL_ZONES if not self.zones else self.zones
        return GeoPoliticalZone.objects.filter(name__in=geo_zones)
    
    

class GeoPoliticalZoneField(BaseField):
    """
    A custom form field for selecting a political zones in Nigeria.

    Example usage:
    ```
    zone = GeoPoliticalZoneField(
            label='Zone',
            empty_label='Select a Zone', # the first option in the dropdown
            help_text='Select a zone from the dropdown',
            zones=[PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_EAST],
            widget=forms.Select(attrs={'class': 'select form-select select2'}),
    )
    ```
    """
    def get_choices(self):
        empty_label = self.empty_label or 'Select a Geo-Political Zone'
        choices = [('', empty_label)]
        table_names = connection.introspection.table_names()
        if 'nigerian_states_geopoliticalzone' in table_names:
            qs = GeoPoliticalZone.objects.all()
            if self.geo_political_zones():
                qs = self.geo_political_zones()
            choices += [(zone.name, zone.name) for zone in qs]
        return choices

    
class StateFormField(BaseField):
    """
    A custom form field for selecting a state in Nigeria.This field extends the ChoiceField.
    Reason for using ChoiceField is `State` and `Town` are to be treated as `CharField`.

    Example usage:
    ```
    state = state = StateFormField(
            label='Name of States',
            empty_label = 'Select a State',
            help_text='Select a state from the dropdown',
            zones=[PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_EAST],
            widget=forms.Select(attrs={'class': 'select form-select select2', 'required': 'required'}),
    )
    ```
    #todo: Add default `state` and `lga`, the default would be preselected on the fields.
    """
    def get_choices(self):
        empty_label = self.empty_label or 'Select a State from the dropdown'
        choices = [('', empty_label)]
        table_names = connection.introspection.table_names()
        if 'nigerian_states_state' in table_names:
            qs = State.objects.all()
            if self.geo_political_zones():
                qs = qs.filter(zone__in=self.geo_political_zones())
            choices += [(state.name, state.name) for state in qs]
        return choices
        

class LocalGovernmentField(BaseField):
    """
    A custom form field for selecting Local Governments in Nigeria.
    Example usage:
    ```
    lga = LocalGovernmentField(label='Local Governments',
                                help_text='Select a LGA from the dropdown', 
                                zones=[PoliticalZones.NORTH_CENTRAL, PoliticalZones.NORTH_EAST],
                                widget=forms.Select(attrs={'class': 'select form-select select2', 'required': 'required'}))
    ```
    """
    
    def get_choices(self):
        empty_label = self.empty_label or 'Select a LG from the dropdown'
        choices = choices = [('', empty_label)]
        table_names = connection.introspection.table_names()
        if 'nigerian_states_localgovernment' in table_names:
            qs = LocalGovernment.objects.all()
            if self.geo_political_zones():
                qs = qs.filter(state__zone__in=self.geo_political_zones())
            choices += [(lga.name, f"{lga.state.name}: {lga.name}") for lga in qs]
        return choices