from django.urls import path
from .import views

urlpatterns = [
  

  path('api/login/', views.LoginView.as_view(), name='login'),
  path('notifications/', views.get_notifications, name='get_notifications'),
  path('enquiries_post/', views.Enquiry_post),
  # path('enquiries_get/<int:pk>/', views.Enquiry_get),
  path('enquiries_put/<int:pk>/', views.Enquiry_put),
  path('enquiryview/', views.enquiryList, name='get_enquiryList'),
  path('enquiries_delete/<int:pk>/', views.Enquiry_delete, name='enquiry-delete'),
    # Add other paths here

]