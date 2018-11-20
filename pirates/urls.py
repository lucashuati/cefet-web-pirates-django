from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaTesourosView.as_view(), name='list'),
    path('new', views.SalvarTesouroView.as_view(), name='new'),
]
