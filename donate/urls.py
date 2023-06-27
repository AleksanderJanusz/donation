from django.urls import path
from donate import views

urlpatterns = [
    path('add-donation/', views.AddDonation.as_view(), name='add_donation'),
]
