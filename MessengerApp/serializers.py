from rest_framework import serializers
from .models import UsersDatabase

class UsersDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersDatabase
        fields = ['id', 'Name', 'username', 'Date', 'Note']