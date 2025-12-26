from django.contrib import admin
from django.urls import path
from attestation.views import verify_integrity
from attestation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/verify/', verify_integrity),
    path('api/logs/', views.get_logs, name='get_logs'), 
    path('resolve/<int:log_id>/', views.resolve_tamper),
]
