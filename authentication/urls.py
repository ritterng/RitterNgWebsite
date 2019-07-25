from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('profile/',views.profile,name='profile'),
    path('register/', views.register_user, name='register'),
    path('edit-profile/',views.edit_profile, name='edit-profile'),
    path('change-password/', views.change_password, name='change-password'),
]
