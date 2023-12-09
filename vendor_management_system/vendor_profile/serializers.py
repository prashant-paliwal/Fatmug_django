from rest_framework import serializers
from .models import Vendor, HistoricalPerformance
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'user_permissions')

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'

class VenderPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
