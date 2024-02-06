from django.core.exceptions import ValidationError
from nigerian_states.models import GeoPoliticalZone, State, LocalGovernment
from django.test import TestCase, override_settings
from django.db.models import QuerySet
from django.conf import settings

from nigerian_states.utils import queryset_to_list
from .defaults import FIRST_LG, FIRST_STATE, FIRST_THREE_STATE, LAST_LG, LAST_STATE, LAST_THREE_STATE, load_fixtures, get_random_lga, get_random_state, get_random_zone, TOTAL_ZONES, TOTAL_STATES, TOTAL_LGAS    
from django import forms

from nigerian_states.fields import BaseField, GeoPoliticalZoneField, StateField, LocalGovernmentField


DEFAULT_POLITICAL_ZONES = getattr(settings, 'DEFAULT_GEO_POLITICAL_ZONES', [])
class BaseFieldTestCase(TestCase):
    
    
    def test_base_field_before_loading_data(self):
        field = BaseField()
        self.assertListEqual(field.zones, [])
        self.assertEqual(field.empty_label, None)
        self.assertEqual(field.geo_political_zones().count(), 0)
        self.assertIsInstance(field.geo_political_zones(), QuerySet)
        self.assertListEqual(field.choices, [('', '')])
        self.assertListEqual(field.choices, field.get_choices())

class GeoPoliticalFieldTestCase(TestCase):
    """
    Test Case for GeoPoliticalZone before loading data in the db yet.
    """

    def test_geo_political_zone_initialization_without_data(self):
        field = GeoPoliticalZoneField()
        # print(getattr(settings, 'DEFAULT_GEO_POLITICAL_ZONES', []))
        self.assertIsInstance(field, GeoPoliticalZoneField)
        self.assertEqual(field.empty_label, None)
        self.assertEqual(field.zones, [])
        self.assertEqual(field.choices, [('', 'Select a Geo-Political Zone')])
        with self.assertRaises(ValidationError):
            field.clean("Sokoto")
        self.assertEqual(field.geo_political_zones().count(), 0)
        self.assertEqual(len(field.get_choices()), 1)
        
    def test_geo_political_zone_initialization_with_data(self):
        """
        Test the initialization of GeoPoliticalZoneField with data in DB.
        """
        load_fixtures()
        field = GeoPoliticalZoneField()
        default_zone = sorted(getattr(settings, 'DEFAULT_GEO_POLITICAL_ZONES', []))
        """ DEFAULT_GEO_POLITICAL_ZONES = ['North West', 'South South'] """
        default_zone = GeoPoliticalZone.objects.filter(name__in=default_zone)
        default_choices = [('', 'Select a Geo-Political Zone')]
        default_choices += [(zn.name, zn.name) for zn in default_zone]
        # print(getattr(settings, 'DEFAULT_GEO_POLITICAL_ZONES', []))
        self.assertIsInstance(field, GeoPoliticalZoneField)
        self.assertEqual(field.empty_label, None)
        self.assertEqual(field.zones, [])
        self.assertEqual(field.choices[0], ('', 'Select a Geo-Political Zone'))
        self.assertEqual(field.geo_political_zones().count(), 2)
        self.assertEqual(len(field.get_choices()), 3)
        self.assertListEqual(field.get_choices(), default_choices)
        self.assertEqual(queryset_to_list(field.geo_political_zones(), 'name'), queryset_to_list(default_zone, 'name'))
        a_choice = default_choices[1][0]
        self.assertEqual(field.clean(a_choice), a_choice)
        with self.assertRaises(ValidationError):
            self.assertEqual(field.clean('North Central'), 'North Central')
            
    @override_settings(DEFAULT_GEO_POLITICAL_ZONES=[])
    def test_geo_political_zone_field_without_zone(self):
        """
        Test the GeoPoliticalZoneField without default zones, or kwargs zones, or Zones in DB
        """
        field = GeoPoliticalZoneField()
        self.assertEqual(len(field.choices), field.geo_political_zones().count() + 1) # the empty label
        self.assertListEqual(field.choices, [('', 'Select a Geo-Political Zone')])
        with self.assertRaises(ValidationError):
            field.clean('North Central')
            
    def test_geo_political_zone_initialization_with_data_and_kwargs(self):
        """
        Test GeoPoliticalZoneField with kwargs (label, empty_label, zones, widget etc.) with data in DB
        """
        load_fixtures()
        zones = ['North Central', 'North West', 'South East']
        field = GeoPoliticalZoneField(
            label = 'GeoPolitical Zone',
            empty_label = 'Select a Zone',
            zones = zones,
            help_text = 'Select a GeoPolitical Zone',
            widget=forms.Select(attrs={'class': 'form-select'})
        )
        self.assertEqual(field.label, 'GeoPolitical Zone')
        self.assertEqual(field.empty_label, 'Select a Zone')
        self.assertListEqual(field.zones, zones)
        self.assertEqual(field.help_text, 'Select a GeoPolitical Zone')
        self.assertTupleEqual(field.choices[0], ('', 'Select a Zone'))
        with self.assertRaises(ValidationError):
            field.clean('North North')
        self.assertNotIn(('North North', field.choices))
        self.assertListEqual(sorted(field.zones), sorted(queryset_to_list(field.geo_political_zones(), 'name')))
        self.assertEqual(field.clean('South East'), 'South East')
        self.assertEqual(len(field.choices), len(zones) + 1)
        # Testing the Widget.
        widget = field.widget
        self.assertIsInstance(widget, forms.Select)
        self.assertEqual(widget.attrs['class'], 'form-select')
        

        
        
        
class FieldTestCase(TestCase):
    """
    Test cases for the custom fields
    """
    def setUp(self):
        load_fixtures()