from django.urls import path
from donate import views

urlpatterns = [
    path('inst-api/', views.InstitutionPaginatorAPI.as_view(), name='inst_api'),

    path('add-donation/', views.AddDonation.as_view(), name='add_donation'),
]
