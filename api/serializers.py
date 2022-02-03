from rest_framework import serializers
from users.models import User

class ReceiveDataSerializer(serializers.Serializer):
    assembly = serializers.IntegerField(required = True)
    part = serializers.DictField(required=True)
    voter_list = serializers.ListField(child = serializers.DictField(),required=True)
    
class RegistrationAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")
   