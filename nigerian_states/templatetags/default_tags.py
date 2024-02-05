from django import template
from django.conf import settings
from nigerian_states.enums import PoliticalZones
from nigerian_states.models import GeoPoliticalZone, State, LocalGovernment
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.simple_tag
def get_states_in_zone(zone_name):
    """
    get the list of states in a geopolitical zone

    Args:
        zone (str): Geopolitical zone

    Returns:
        list: List of state in the Geopolitical zone
    """
    zones = PoliticalZones.values
    if zone_name not in zones:
        return []
    try:
        zone = GeoPoliticalZone.objects.get(name=zone_name)
    except GeoPoliticalZone.DoesNotExist:
        return []
    return list(zone.all_states.values_list('name', flat=True))


@register.simple_tag
def get_capital(state_name):
    """
    Returns the capital of the state provided

    Args:
        state_name (str): Name of the state

    Returns:
        str: capital of the state
    """
    try:
        state = State.objects.get(name=state_name)
    except State.DoesNotExist:
        return None
    return state.capital


@register.simple_tag
def get_lgas_in_state(state_name):
    """
    get the list of LG in the provided state name

    Args:
        state_name (str): Name of the state

    Returns:
        list: List of local government in the state
    """
    try:
        state = State.objects.get(name=state_name)
    except State.DoesNotExist:
        return []
    return list(state.lgas.values_list('name', flat=True))

@register.simple_tag
def is_state_in_zone(zone_name, state_name):
    """
    check to see if the state is from the zone

    Args:
        state_name (str): name of state
        zone_name (str): name of geopolitical zone

    Returns:
        bool: True if state is from the zone_name else False
    """
    try:
        state = State.objects.get(name=state_name)
        zone = GeoPoliticalZone.objects.get(name=zone_name)
    except ObjectDoesNotExist:
        return False
    return state.zone.name == zone.name


@register.simple_tag
def is_lga_in_state(state_name, lga_name):
    """
    check whether the lga name is from the state

    Args:
        state_name (str): name of the state
        lga_name (str): name of the local government

    Returns:
        bool: True if lga is under the state.
    """
    try:
        state = State.objects.get(name=state_name)
        lga = LocalGovernment.objects.get(name=lga_name)
    except ObjectDoesNotExist:
        return False
    return lga in state.lgas
    
    
@register.filter
def default_zone():
    return getattr(settings, 'DEFAULT_GEO_POLITICAL_ZONES', [])


@register.simple_tag
def get_zone(state):
    """
    returns the name of the zone the state belongs to

    Args:
        state (State): name of the state
        
    Returns:
        str: geopolitical zone of the state
    """
    try:
        state = State.objects.get(name=state)
    except State.DoesNotExist:
        return None
    return state.zone.name

@register.simple_tag
def get_zone_info(zone_name):
    try:
        zone = GeoPoliticalZone.objects.get(name=zone_name)
    except GeoPoliticalZone.DoesNotExist:
        return {}
    state_ids = list(zone.all_states.values_list('id', flat=True))
    lgas = list(LocalGovernment.objects.filter(state__in=state_ids).values_list('name', flat=True))
    output = {
        'zone': zone.name,
        'no_of_states': zone.all_states.count(),
        'states': list(zone.all_states.values_list('name', flat=True)),
        'no_of_lgas': lgas.count(),
        'lgas': lgas
    }
    return output