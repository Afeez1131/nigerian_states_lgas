from django.contrib import admin
from nigerian_states.models import State, LocalGovernment, GeoPoliticalZone


@admin.register(GeoPoliticalZone)
class GeoPoliticalZoneAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["name", "capital", "zone"]


@admin.register(LocalGovernment)
class LocalGovernmentAdmin(admin.ModelAdmin):
    pass
