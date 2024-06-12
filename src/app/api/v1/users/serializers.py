from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("id", "username", "password", "email")
        read_only_fields = ["id"]
        write_only_fields = ["password"]
