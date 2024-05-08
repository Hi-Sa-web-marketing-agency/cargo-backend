from django.urls import path
from .import views

urlpatterns = [
  

  path('api/login/', views.LoginView.as_view(), name='login'),
]