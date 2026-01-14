from django.urls import path
from .views import PhoneInfoAPIView

urlpatterns = [
    path('check-phone/', PhoneInfoAPIView.as_view(), name='check_phone'),
]