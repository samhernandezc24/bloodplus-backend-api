from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from bloodplus_v1.models import User, Location, BloodType
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/v1/usuarios/',
        '/api/v1/usuarios/crear/',
        '/api/v1/token',
        '/api/v1/token/refresh',
        '/api/v1/token/verify',
    ]

    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    role = request.query_params.get('role', None)
    if role and role in ['DONADOR', 'SOLICITADOR']:
        users = User.objects.filter(role=role)
    else:
        users = User.objects.filter(role__in=['DONADOR', 'SOLICITADOR'])

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_create_view(request):
    data = request.data
    serializer = SignUpSerializer(data=data)

    if serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            role = data.get('role', User.Role.ADMIN)
            blood_type = None

            if role != User.Role.ADMIN:
                try:
                    blood_type = BloodType.objects.get(id=data['blood'])
                except BloodType.DoesNotExist:
                    return Response({'error': 'El tipo de sangre proporcionado no existe'}, status=status.HTTP_400_BAD_REQUEST)

            user_data = {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'username': data['email'],
                'email': data['email'],
                'password': make_password(data['password']),
                'role': role,
                'date_of_birth': data['date_of_birth'],
            }

            if blood_type:
                user_data.update({
                    'gender': data['gender'],
                    'blood': blood_type,
                    'phone': data['phone'],
                })

            User.objects.create(**user_data)

            return Response({
                'message': 'Tu registro ha sido exitoso. ¡Bienvenido(a) a BloodPlus!'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                'error': 'Parece que ya existe un usuario con las mismas credenciales que estás intentando utilizar. Por favor, asegúrate de que has ingresado correctamente la información o intenta utilizar diferentes credenciales.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CurrentUserView(request):
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data)
