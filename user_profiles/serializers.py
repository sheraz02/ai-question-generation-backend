from rest_framework import serializers
from user_profiles.models import User, TestSession


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        # if User.objects.filter(email=attrs["email"]).exists():
        #     raise serializers.ValidationError({"email": "Email already exists"})

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return attrs


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


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestSession
        fields = ['questionsSet']