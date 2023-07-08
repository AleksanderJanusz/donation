from django.urls import path
from donate import views

urlpatterns = [
    path('inst-api/', views.InstitutionPaginatorAPI.as_view(), name='inst_api'),

    path('add-donation/', views.AddDonation.as_view(), name='add_donation'),
    path('profile/', views.Profil.as_view(), name='profile'),
    path('donate/<int:pk>/', views.DonateDetails.as_view(), name='donate_details'),
]
