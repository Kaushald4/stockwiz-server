from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['email', 'password', 'name']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    
class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
