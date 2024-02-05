from nigerian_states.models import State, LocalGovernment
from django.test import TestCase, override_settings
from django.conf import settings
from django.core.management import call_command
import os


EXPECTED_STATE_COUNT = 37
FIRST_STATE = "Adamawa"
LAST_STATE = "Abia"


class TestStateModel(TestCase):
    print('here...')
    """
    Test cases for the State Model
    """
    @override_settings(DISABLE_SIGNAL_LOAD_DATA=True)
    def setUp(self):
        pass
            
    def tearDown(self):
        pass
    
    @override_settings(DISABLE_SIGNAL_LOAD_DATA=True)
    def test_state_before_loading_data(self):
        """
        Test state model before loading data on it.
        """
        self.assertFalse(State.objects.exists())
        
    
    def test_state_after_migration(self):
        pass