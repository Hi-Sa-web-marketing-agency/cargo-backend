from django.urls import path
from .import views

urlpatterns = [
  

  path('api/login/', views.LoginView.as_view(), name='login'),
  path('notifications/', views.get_notifications, name='get_notifications'),
  path('enquiries/', views.EnquiryAPIView.as_view()),
  path('enquiries/<int:pk>/', views.EnquiryAPIView.as_view()),
  path('enquiryview/', views.enquiryList, name='get_enquiryList'),

]