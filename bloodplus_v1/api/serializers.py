from django.contrib.auth import get_user_model
from rest_framework import serializers
from bloodplus_v1.models import Location, BloodType

User = get_user_model()


class AdminSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
        }


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password', 'phone', 'gender', 'blood',
            'location', 'date_of_birth',
        ]
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
            'phone': {'required': False, 'allow_blank': True},
            'gender': {'required': True},
            'blood': {'required': True},
            'location': {'required': False},
            'date_of_birth': {'required': True},
        }


class SignUpSerializer(serializers.ModelSerializer):
    role = serializers.CharField()

    def validate_role(self, value):
        valid_roles = ['ADMIN', 'DONADOR', 'SOLICITADOR']

        if value not in valid_roles:
            raise serializers.ValidationError('Tipo de rol inválido.')
        return value

    def to_internal_value(self, data):
        role = data.get('role')

        if role == 'ADMIN':
            role_serializer = AdminSignUpSerializer(data=data)
        else:
            role_serializer = UserSignUpSerializer(data=data)

        role_serializer.is_valid(raise_exception=True)
        return role_serializer.validated_data


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('address', 'zip_code', 'country', 'state')


class BloodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodType
        fields = ('blood_type', 'description')


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
