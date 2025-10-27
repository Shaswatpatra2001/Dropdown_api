from django.urls import path
from .views import LocationAPIView

urlpatterns = [
    path('locations/', LocationAPIView.as_view(), name='locations-api'),
]