from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Book, Order, Rating

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=User.Roles.USER
        )
        return user

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role'],
            is_staff=validated_data['role'] == User.Roles.ADMIN,
            is_superuser=validated_data['role'] == User.Roles.ADMIN
        )
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'daily_price', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'book', 'status', 'reserve_time', 'taken_time', 'return_time', 'fine']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'status': {'read_only': True},
            'reserve_time': {'read_only': True},
            'taken_time': {'read_only': True},
            'return_time': {'read_only': True},
            'fine': {'read_only': True}
        }

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'book', 'score', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True}
        }

    def validate_score(self, value):
        if not 0 <= value <= 5:
            raise serializers.ValidationError("Score must be between 0 and 5")
        return value