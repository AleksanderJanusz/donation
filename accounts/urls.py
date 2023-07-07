from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('edit/', views.Edit.as_view(), name='edit'),
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('activate/<token>', views.Activate.as_view(), name='activate'),
    path('recover-password-token/', views.PasswordRecoveryToken.as_view(), name='recover_password_token'),
    path('recover-password/<token>', views.PasswordRecovery.as_view(), name='password_recovery'),
]
