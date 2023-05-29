from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from ..serializers import SignUpSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated

from bloodplus_v1.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom class
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/v1/token',
        '/api/v1/token/refresh',
    ]

    return Response(routes)


@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['username'],
                email=data['email'],
                password=make_password(data['password']),
            )
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
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUser(request):
    user = UserSerializer(request.user)
    return Response(user.data)
