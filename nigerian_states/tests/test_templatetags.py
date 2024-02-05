from django.test import TestCase

from nigerian_states.models import State
from .defaults import get_state, load_fixtures, get_random_state_in_zone
from django.template import Context, Template
from nigerian_states.templatetags.default_tags import get_capital, get_lgas_in_state, get_states_in_zone, get_zone, is_lga_in_state, is_state_in_zone

class TestTemplateTags(TestCase):
    """
    Test cases for the template tags
    """
    def setUp(self):
        load_fixtures()
        
        
    # def test_tags_get_states(self):
        """
        I don't think you need to render a template in order to test your filter logic. Django already has well-tested template rendering logic, which the unit-tests for your filter shouldn't have to worry about since the "job" done by your filter is not to render to a template, but to take an input and return an output.
        
        https://stackoverflow.com/questions/49603388/test-a-custom-template-tag-filter-in-django
        """
        """
        # Test that `get_states` template tags returns states from the zone name passed as args.
        # """
        # zone_name = "North Central"
        # state = get_random_state_in_zone(zone_name)
        # context = Context({'zone_name': zone_name})
        # self.GET_STATES = Template(
        #     "{% load default_tags %}{% get_states_in_zone zone_name as states %}{{ states|safe }}"
        # )
        # rendered = self.GET_STATES.render(context)
        # self.assertIn(state.name, rendered)
        
    def test_tag_get_state_in_zone(self):
        """
        Test that template tag `get_states_in_zones` return the expected output.
        """
        zone_name = 'North Central'
        state = get_random_state_in_zone(zone_name)
        states_in_zones = get_states_in_zone(zone_name)
        self.assertIsInstance(states_in_zones, list)
        self.assertIn(state.name, states_in_zones)
        self.assertEqual(len(State.objects.filter(zone__name=zone_name)), len(states_in_zones))
        
    def test_tag_get_capital(self):
        """
        Test that the `get_capital` returns the right capital for the state
        """
        state = State.objects.get(name='Lagos')
        self.assertIsInstance(get_capital(state.name), str)
        self.assertEqual(get_capital(state.name), 'Ikeja')
        self.assertEqual(get_capital('Oyo'), 'Ibadan')
        self.assertEqual(get_capital('Kwara'), 'Ilorin')
        
    def test_tag_get_lgas_in_state(self):
        """
        Test that the tag `get_lgas_in_state` returns all lgas in a state.
        """
        oyo_state = get_state("Oyo")
        all_lgas_oyo = get_lgas_in_state(oyo_state.name)
        self.assertIsInstance(get_lgas_in_state(oyo_state.name), list)
        self.assertIn('Ogbomosho North', get_lgas_in_state(oyo_state.name))
        self.assertEqual(len(all_lgas_oyo), oyo_state.total_lgas)
        
        lagos = get_state("Lagos")
        all_lgas_lagos = get_lgas_in_state(lagos.name)
        self.assertIsInstance(get_lgas_in_state(lagos.name), list)
        self.assertIn('Badagry', get_lgas_in_state(lagos.name))
        self.assertEqual(len(all_lgas_lagos), lagos.total_lgas)
        
    def test_tag_is_state_in_zone(self):
        """
        Test that tag returns True if a state is in a zone or False if not.
        """
        self.assertIsInstance(is_state_in_zone('South West', 'Oyo'), bool)
        self.assertTrue(is_state_in_zone('South West', 'Oyo'))  
        self.assertTrue(is_state_in_zone('South West', 'Lagos')) 
        self.assertTrue(is_state_in_zone('North West', 'Kano')) 
        self.assertFalse(is_state_in_zone('South South', 'Oyo'))
        
    def test_tag_is_lga_in_state(self):
        """
        Test that tag `is_lga_in_state` returns True if lga is in state else False
        """
        self.assertIsInstance(is_lga_in_state('Oyo', 'Surulere'), bool)
        self.assertTrue(is_lga_in_state('Oyo', 'Ogbomosho North'))  
        self.assertTrue(is_lga_in_state('Abia', 'Aba South')) 
        self.assertTrue(is_lga_in_state('Kano', 'Ungogo')) 
        self.assertFalse(is_lga_in_state('Lagos', 'Invalid LGA'))
        
    def test_tag_get_zone(self):
        """
        Test that tag `get_zone` returns the name of the zone the state belongs to if a valid state, else None
        """
        self.assertEqual(get_zone('Oyo'), 'South West')
        self.assertEqual(get_zone('Lagos'), 'South West')
        self.assertEqual(get_zone('Kano'), 'North West')
        self.assertEqual(get_zone('Invalid State'), None)
        
    def test_tag_get_zone_info(self):
        """
        Test that the `get_zone_info` returns 
        {
            "zone": zone name,
            "no of states": no of states,
            "states": [list of states]
            "no of lgas": no of lgas,
            "lgas": [list of lgas]
        }
        if valid zone name else {}
        """
        pass