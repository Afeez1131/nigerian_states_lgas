from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('update/<int:pk>', views.update_about, name='update_about'),
]
