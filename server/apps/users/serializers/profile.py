from rest_framework.serializers import ModelSerializer

from apps.users.models.profile import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'bio', 'img', 'following',)
        extra_kwargs = {'user': {'read_only': True}}

    def update(self, instance, validated_data):
        if 'bio' in validated_data:
            instance.bio = validated_data['bio']
        if 'img' in validated_data:
            instance.img = validated_data['img']
        if 'following' in validated_data:
            instance.following.set(validated_data['following'])
        instance.save()

        return instance
