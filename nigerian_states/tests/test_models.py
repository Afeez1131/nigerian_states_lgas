from nigerian_states.models import GeoPoliticalZone, State, LocalGovernment
from django.test import TestCase, override_settings
from django.conf import settings
from django.core.management import call_command
import random


EXPECTED_STATE_COUNT = 37
FIRST_STATE = "Abia"
FIRST_LG = "Aba North"
LAST_LG = "Municipal Area Council"
LAST_STATE = "Federal Capital Territory"
TOTAL_ZONES = 6
TOTAL_STATES = 37
TOTAL_LGAS = 774
FIRST_THREE_STATE = ['Abia', 'Adamawa', 'Akwa Ibom']
LAST_THREE_STATE = ['Federal Capital Territory', 'Zamfara', 'Yobe']

def get_random_zone():
    return random.choice(GeoPoliticalZone.objects.all())
    
    
def get_random_state():
    return random.choice(State.objects.all())

def get_random_lga():
    return random.choice(LocalGovernment.objects.all())

def load_fixtures():
    """
    Helper function to load fixtures data in the needed test function
    """
    return call_command('loaddata', 'nigerian_states/fixtures/fixtures.json', verbosity=0)
    

class TestGeoPoliticalZone(TestCase):
    """
    Test cases for GeoPoliticalZone model.
    """
    def setUp(self):
        load_fixtures()



    # def test_zones_model_without_data(self):
    #     """
    #     Test the GeoPoliticalZone model without data in it.
    #     """
    #     self.assertFalse(GeoPoliticalZone.objects.exists())
    #     self.assertEqual(GeoPoliticalZone.objects.count(), 0)
        
    def test_zone_string_representation(self):
        """
        Test the string representation of GeoPoliticalZone model
        """
        zone = GeoPoliticalZone.objects.get(name='North Central')
        self.assertEqual(str(zone), 'North Central')
        
    
    def test_zone_has_all_states_property(self):
        """
        Test that GeoPoliticalZone has the `all_states` property.
        """
        zone = get_random_zone()
        self.assertTrue(hasattr(zone, 'all_states'))
        
    def test_total_number_of_zones(self):
        """
        Test the total number of zones
        """
        zones_count = GeoPoliticalZone.objects.count()
        self.assertEqual(zones_count, TOTAL_ZONES)
        
    def test_all_states_property(self):
        """
        Test that the `all_states` property returns all the state in a GeoPoliticalZone
        """
        zone = get_random_zone()
        zone_state = zone.all_states.values_list('id', flat=True)
        s_state = State.objects.filter(zone=zone).values_list('id', flat=True)
        self.assertEqual(len(zone_state), len(s_state))
        self.assertEqual(len(set(zone_state).difference(set(s_state))), 0)
        self.assertEqual(zone.all_states.count(), State.objects.filter(zone=zone).count())
        
    def test_fetching_zone_with_invalid_name(self):
        """
        Test that fething GeoPoliticalZone with invalid name would raise DoesNotExist exception.
        """
        with self.assertRaises(GeoPoliticalZone.DoesNotExist):
            GeoPoliticalZone.objects.get(name='Invalid zone name')
        
    def test_fetching_zone_with_valid_name(self):
        self.assertTrue(GeoPoliticalZone.objects.filter(name='North Central').exists())
        
    def test_all_lgas_in_zones(self):
        """
        Test that all lgas in a zone is right.
        """
        zone = get_random_zone()
        lgas = LocalGovernment.objects.filter(state__zone=zone)
        all_state_ids = zone.all_states.values_list('id', flat=True)
        all_lgas = LocalGovernment.objects.filter(state__in=all_state_ids)
        self.assertEqual(lgas.count(), all_lgas.count())
        self.assertEqual(len(set(lgas).difference(set(all_lgas))), 0)
        
    def test_zone_has_reverse_foreignKey_relation_to_state(self):
        """
        test that GeoPoliticalZone has a reverse foreignkey relationship to state
        """
        zone = get_random_zone()
        self.assertTrue(zone.states.all())
    
        
        
class TestStateModel(TestCase):
    """
    Test cases for the State Model
    """
    def setUp(self):
        load_fixtures()

            
    
    # def test_state_before_loading_data(self):
    #     """
    #     Test state model before loading data on it.
    #     """
    #     self.assertFalse(State.objects.exists())
    #     self.assertEqual(State.objects.count(), 0)
    
    def test_state_string_representation(self):
        state = State.objects.get(name='Lagos')
        self.assertEqual(str(state), 'Lagos')
        
    def test_state_has_property_total_lgas(self):
        """
        Test that State has propety `total_lgas`
        """
        state = get_random_state()
        self.assertTrue(hasattr(state, 'total_lgas'))
        
    def test_state_has_property_lgas(self):
        """
        Test that State has property `lgas`
        """
        state = get_random_state()
        self.assertTrue(hasattr(state, 'lgas'))
        
    def test_state_lgas_property(self):
        """
        Test that the `lgas` property returns all lga in a state
        """
        state = get_random_state()
        lgas = LocalGovernment.objects.filter(state=state)
        self.assertEqual(state.lgas.count(), lgas.count())
        
        
    def test_total_number_of_state(self):
        """
        Test the total number of states
        """
        state_count = State.objects.count()
        self.assertEqual(state_count, TOTAL_STATES)
        
    def test_total_number_of_lgas_in_state(self):
        """
        Test to confirm the `state.lgas` is equal to LocalGovernement.filter(state)
        """
        state = get_random_state()
        all_lgas_prop = state.lgas
        lgas = LocalGovernment.objects.filter(state=state)
        self.assertEqual(all_lgas_prop.count(), lgas.count())
        self.assertEqual(len(set(all_lgas_prop).difference(set(lgas))), 0) # they are the same.
        
    def test_first_state_name(self):
        first_state = State.objects.get(id=1)
        self.assertEqual(first_state.name, FIRST_STATE)
        
    def test_first_three_states_names(self):
        state = State.objects.values_list('name', flat=True)[:3]
        self.assertEqual(list(state), FIRST_THREE_STATE)
        
    def test_last_state_name(self):
        last_state = State.objects.get(id=37)
        self.assertEqual(last_state.name, LAST_STATE)
        
    def test_last_three_states_names(self):
        last_three = State.objects.order_by('-id').values_list('name', flat=True)[:3]
        self.assertEqual(list(last_three), LAST_THREE_STATE)
        
    def test_fetching_state_with_invalid_name(self):
        """
        Test that getting state with an invalid name wold raise DoesNotExist exception
        """
        with self.assertRaises(State.DoesNotExist):
            State.objects.get(name='Invalid name')
            
    def test_state_has_foreignkey_relation_to_zone(self):
        """
        """
        state = get_random_state()
        self.assertIsInstance(state.zone, GeoPoliticalZone)
        
    def test_state_has_reverse_foreignkey_relation_to_lga(self):
        state = get_random_state()
        self.assertTrue(state.localgovernment_set.all())
        
        
class TestLocalGovernmentModel(TestCase):
    """
    Test cases for the LocalGovernment Model
    """
    def setUp(self):
        load_fixtures()

            
    
    # def test_state_before_loading_data(self):
    #     """
    #     Test state model before loading data on it.
    #     """
    #     self.assertFalse(State.objects.exists())
    #     self.assertEqual(State.objects.count(), 0)
    
    def test_state_string_representation(self):
        lg = LocalGovernment.objects.get(name='Aba South')
        self.assertEqual(str(lg), f'{lg.state.name}: Aba South')
        
        
    def test_total_lgas(self):
        """
        Test that the total count of LocalGovernment is the expected count.
        """
        lgas = LocalGovernment.objects.count()
        self.assertEqual(lgas, TOTAL_LGAS)
        
    def test_fetching_lgas_with_valid_name(self):
        """
        Test getting LGA with a valid LGA name.
        """
        lga = LocalGovernment.objects.filter(name='Aba South')
        self.assertTrue(lga.exists())
        
    def test_fetching_lgas_with_invalid_name(self):
        """
        Test that fetching LGA with invalid name raises DoesNotExist exception
        """
        with self.assertRaises(LocalGovernment.DoesNotExist):
            LocalGovernment.objects.get(name='invalid name')
            
    def test_first_lg_name(self):
        """
        confirm the LocalGovernment name for the first.
        """
        first_lg = LocalGovernment.objects.first()
        self.assertEqual(first_lg.name, FIRST_LG)
        
    def test_last_lg_name(self):
        """
        confirm the LocalGovernment name for the last LocalGovernment
        """
        last_lg = LocalGovernment.objects.last()
        self.assertEqual(last_lg.name, LAST_LG)
        
    def test_first_lg_state(self):
        """
        confirm the state of the first LocalGovernment is FIRST_STATE
        """
        first_lg = LocalGovernment.objects.first()
        self.assertTrue(first_lg.state.name == FIRST_STATE)
    
    def test_last_lg_state(self):
        """
        confirm the state of the last LocalGovernment is LAST_STATE
        """
        last_lg = LocalGovernment.objects.last()
        self.assertTrue(last_lg.state.name == LAST_STATE)
        
    def test_lg_has_foreignkey_relation_to_state(self):
        lg = get_random_lga()
        self.assertIsInstance(lg.state, State)