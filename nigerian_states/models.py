from django.db import models
from nigerian_states.enums import PoliticalZones


class State(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    zone = models.CharField(max_length=55, choices=PoliticalZones.choices)
    
    def __str__(self):
        return self.name
    
    @property
    def total_lgas(self):
        return self.localgovernment_set.count()


class LocalGovernment(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    
    def __str__(self):
        return f"{self.state.name}: {self.name}"
    
    
class AppSetup(models.Model):
    is_data_loaded = models.BooleanField(default=False)