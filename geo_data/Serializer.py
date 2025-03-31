from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError
from django.conf import settings
from utility import get_location_from_ip,get_client_ip
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        request = self.context.get("request")
        ip_address = get_client_ip(request)
        location_data = get_location_from_ip(ip_address)
        
        allowed_countries = settings.ALLOWED_COUNTRIES

        if allowed_countries and location_data.get("country_code") not in allowed_countries:
            raise serializers.ValidationError("Registration from this country is not allowed.")

        if len(data['password']) < 8:
            raise ValidationError("Password must be at least eight characters long.")

        if data['confirm_password'] != data['password']:
            raise ValidationError("Confirm password and password must match.")
        
        

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user