from rest_framework import serializers
from .models import KBEntry


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class KBQuerySerializer(serializers.Serializer):
    search = serializers.CharField(max_length=255, trim_whitespace=True)

    def validate_search(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value


class KBEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = KBEntry
        fields = [
            "id",
            "question",
            "answer",
            "category",
        ]
