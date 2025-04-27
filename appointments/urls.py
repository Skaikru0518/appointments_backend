from django.urls import path
from . import views
from .views import RegisterView, current_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #Kliens végpontok
    path('clients/', views.getClients, name='client-list'),
    path('clients/<int:pk>/', views.client_detail, name='client-detail'),

    #Masszőrök
    path('workers/', views.worker_list, name="worker-list"),

    #Regisztráció az admin felülethez
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),

    #User adatok
    path('auth/me/', current_user, name="current-user"),

    #Időpont végpontok
    path('appointments/', views.appointment_list, name='appointment-list'),
    path('appointments/<int:pk>/', views.appointent_detail, name='appointment-detail'),
    path('appointments/upcoming/', views.upcoming_appointments, name='upcoming-appointments')
]