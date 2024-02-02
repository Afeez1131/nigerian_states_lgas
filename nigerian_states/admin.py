from django.contrib import admin
from nigerian_states.models import State, LocalGovernment, AppSetup


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(LocalGovernment)
class LocalGovernmentAdmin(admin.ModelAdmin):
    pass