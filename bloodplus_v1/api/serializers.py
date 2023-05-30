from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from rest_framework import serializers
from bloodplus_v1.models import Location, BloodType

User = get_user_model()


class BloodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodType
        fields = ('blood_type', 'description')


class AdminSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name',
                  'last_name', 'date_of_birth']
        extra_kwargs = {
            'email': {'validators': [EmailValidator()]},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'date_of_birth': {'required': True}
        }


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password', 'phone', 'gender', 'blood',
            'location', 'date_of_birth'
        ]
        extra_kwargs = {
            'email': {'validators': [EmailValidator()]},
            'password': {'required': True, 'min_length': 8},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone': {'required': False},
            'gender': {'required': True},
            'blood': {'required': False},
            'location': {'required': False},
            'date_of_birth': {'required': True},
        }


class SignUpSerializer(serializers.ModelSerializer):
    role = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password', 'phone', 'gender', 'blood',
            'location', 'date_of_birth', 'role'
        ]

    def to_representation(self, instance):
        if instance.role == User.Role.ADMIN:
            serializer = AdminSignUpSerializer(instance)
        else:
            serializer = UserSignUpSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        role = validated_data.pop('role')

        if role == User.Role.ADMIN:
            serializer = AdminSignUpSerializer(data=validated_data)
        else:
            serializer = UserSignUpSerializer(data=validated_data)

        serializer.is_valid(raise_exception=True)
        return serializer.save()


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('address', 'zip_code', 'country', 'state')


class UserSerializer(serializers.ModelSerializer):
    GENDER_CHOICES = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
        ('I', 'Indefinido'),
    )
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES, source='get_gender_display')
    role = serializers.CharField(source='get_role_display')
    blood = BloodTypeSerializer()
    location = LocationSerializer()
    total_donations = serializers.SerializerMethodField()
    total_requests = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'phone', 'gender', 'blood', 'date_of_birth', 'location',
                  'average_rating', 'total_donations', 'total_requests', 'role')

    def get_total_donations(self, obj):
        if obj.role == User.Role.DONOR:
            return obj.total_donations
        return None

    def get_total_requests(self, obj):
        if obj.role == User.Role.REQUESTER:
            return obj.total_requests
        return None
