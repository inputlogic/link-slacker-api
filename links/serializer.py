from rest_framework.serializers import ModelSerializer

from .models import URL


class URLSerializer(ModelSerializer):
    class Meta:
        model = URL
        fields = [
            "title",
            "link",
            "description",
            "image",
            "msg",
            "created_on"
        ]

    def create(self, validated_data):
        """
        Create and return a new URL instance, given the validated data.
        """
        return URL.objects.create(**validated_data)
