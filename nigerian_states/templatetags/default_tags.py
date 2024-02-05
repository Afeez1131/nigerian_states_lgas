from django import template
from django.conf import settings
from nigerian_states.enums import PoliticalZones
from nigerian_states.models import State, LocalGovernment
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.simple_tag
def get_state_from_zone(zone):
    zones = PoliticalZones.values
    if zone not in zones:
        return []
    return list(State.objects.filter(zone=zone).values_list('name', flat=True))


@register.simple_tag
def get_state_lgas(state_name):
    try:
        state = State.objects.get(name=state_name)
    except State.DoesNotExist:
        return []
    return list(state.lgas.values_list('name', flat=True))

@register.simple_tag
def is_state_in_zone(state_name, zone_name):
    try:
        state = State.objects.get(name=state_name)
    except State.DoesNotExist:
        return False
    return state.zone == zone_name


@register.simple_tag
def is_lga_in_state(state_name, lga_name):
    try:
        state = State.objects.get(name=state_name)
        lga = LocalGovernment.objects.get(name=lga_name)
    except ObjectDoesNotExist:
        return False
    return lga in state.lgas
    
    
@register.filter
def default_zone():
    return getattr(settings, 'DEFAULT_GEO_POLITICAL_ZONES', [])