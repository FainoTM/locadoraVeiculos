from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cadastrousuario/', views.CadUsuarioView.as_view(), name='cadusuario'),
    path('loginusuario/', views.LoginUserView.as_view(), name='logINusuario'),
    path('logoutinusuario/', views.LogoutUserView.as_view(), name='logOUTusuario'),
]
