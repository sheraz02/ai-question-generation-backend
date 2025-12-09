from rest_framework import serializers
from user_profiles.models import User, TestSession


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return attrs

    # def validate_email(self, value):
    #     # Fix: exclude current instance on update
    #     qs = User.objects.filter(email=value)
    #     if self.instance:
    #         qs = qs.exclude(pk=self.instance.pk)

    #     if qs.exists():
    #         raise serializers.ValidationError("Email already exists")
    #     return value

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]

class TestSessionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TestSession
        fields = ['sessionId', 'user', 'topicsName', 'noOfQuestions', 'difficultyLevel', 'questionsSet']
        read_only_fields = ['sessionId', 'user']
    
    def create(self, validated_data):
        user = self.context.get('user')
        return TestSession.objects.create(user=user, **validated_data)