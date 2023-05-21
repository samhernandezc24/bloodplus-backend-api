from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """
    Crea y guarda un Usuario con la información específica dada.
    """
    def create_user(self, email, username, first_name, last_name, password=None, **other_fields):
        if not email:
            raise ValueError(_('Debe proporcionar una dirección de correo electrónico.'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    """
    Crea y guarda un superusuario con la información correspondiente.
    """
    def create_superuser(self, email, username, first_name, last_name, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'El superusuario debe ser asignado a es is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'El superusuario debe ser asignado a es is_superuser=True')
        return self.create_user(email, username, first_name, last_name, password, **other_fields)
    
class BloodType(models.Model):
    blood_type = models.CharField(max_length=10, blank=True)
    description = models.TextField(_('descripción'), blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'blood_types'

    def __str__(self):
        return self.blood_type
    
class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DONOR = "DONADOR", "Donador"
        REQUESTER = "SOLICITADOR", "Solicitador"

    GENDER_TYPES = (('H', 'Hombre'), ('M', 'Mujer'), ('I', 'Indefinido'))
    email = models.EmailField(_('correo electrónico'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)    
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, default='I')
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)
    blood = models.ForeignKey(BloodType, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(default='2023-02-02')
    average_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0)
    total_donations = models.PositiveIntegerField(default=0)
    total_requests = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username
    
