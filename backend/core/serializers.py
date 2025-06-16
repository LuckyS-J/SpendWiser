from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    # def validate_password(self, value):
    #   validate_password(value)
    #   return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
