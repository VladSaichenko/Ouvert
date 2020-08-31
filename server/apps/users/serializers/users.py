from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, EmailField
from rest_framework.validators import UniqueValidator


class UserSerializer(ModelSerializer):
    email = EmailField(validators=[UniqueValidator(queryset=User.objects.all(), message='This Email is already used')],)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email',)
