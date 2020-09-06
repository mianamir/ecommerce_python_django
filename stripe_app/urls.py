from django.urls import path
from . import views

urlpatterns = [

    path('stripe/index', views.stripe_index, name="stripe_index"),
    path('charge/', views.charge, name="charge"),
    path('success/<str:args>/', views.success_message, name="success"),
]
