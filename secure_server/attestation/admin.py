from django.contrib import admin
from .models import AppVerification, TamperLog

admin.site.register(AppVerification)
admin.site.register(TamperLog)
