from rest_framework import serializers
from .models import AppVerification, TamperLog

class AppVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVerification
        fields = '__all__'

class TamperLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TamperLog
        fields = '__all__'
