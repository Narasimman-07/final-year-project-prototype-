from django.urls import path
from .views import verify_integrity

urlpatterns = [
    path('verify/', verify_integrity, name='verify_integrity'),
]
