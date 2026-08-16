from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import PriceAlert

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = get_user_model()
        fields = ("username", "password", "email")
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class PriceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlert
        fields = ("id", "origin", "destination", "threshold_price", "status", "created_at")
        read_only_fields = ("id", "status", "created_at")
    def validate_origin(self, value):
        return value.upper().strip()
    def validate_destination(self, value):
        return value.upper().strip()
