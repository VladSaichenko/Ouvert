from rest_framework.serializers import ModelSerializer

from apps.users.models.profile import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'bio', 'img', 'following',)
        extra_kwargs = {
            'user': {'read_only': True},
            'id': {'read_only': True},
        }
