from rest_framework.serializers import ModelSerializer

from apps.users.models.profile import UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'bio', 'img',)
        extra_kwargs = {'user': {'read_only': True}}

    def update(self, instance, validated_data):
        print(validated_data)
        if 'bio' in validated_data:
            instance.bio = validated_data['bio']
        if 'img' in validated_data:
            instance.img = validated_data['img']
        instance.save()

        return instance
