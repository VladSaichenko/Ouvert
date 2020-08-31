from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, EmailField


class UserSerializer(ModelSerializer):
    email = EmailField()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',)
