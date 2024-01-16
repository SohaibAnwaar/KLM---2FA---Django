from rest_framework import serializers
from klm.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "name", "email", "fullname"]
