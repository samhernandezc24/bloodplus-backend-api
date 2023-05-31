import geocoder
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Crea y guarda un Usuario con la información específica dada.
    """

    def create_user(self, email, username, first_name, last_name, password=None, **other_fields):
        if not email:
            raise ValueError(
                _('Debe proporcionar una dirección de correo electrónico.'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name, **other_fields)
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


class Location(models.Model):
    address = models.TextField(null=True)
    zip_code = models.CharField(max_length=7, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    point = gismodels.PointField(default=Point(0.0, 0.0))
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'locations'

    def save(self, *args, **kwargs):
        try:
            g = geocoder.mapquest(
                self.address, key=os.environ.get('GEOCODER_API_KEY'))
            lng = g.lng
            lat = g.lat
            print(g)
        except Exception as e:
            lng = 0.0
            lat = 0.0
            print(f"Geocoding error: {str(e)}")

        self.point = Point(lng, lat)
        super(Location, self).save(*args, **kwargs)


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
    role = models.CharField(
        max_length=50, choices=Role.choices, default=Role.ADMIN)
    blood = models.ForeignKey(
        BloodType, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.OneToOneField(
        Location, on_delete=models.RESTRICT, null=True)
    date_of_birth = models.DateField()
    average_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0)
    total_donations = models.PositiveIntegerField(default=0)
    total_requests = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)

    # Modeling Boolean Status: Private Data
    show_email = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=True)
    show_first_name = models.BooleanField(default=True)
    show_last_name = models.BooleanField(default=True)

    date_joined = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth']

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def get_gender_display(self):
        gender_display = dict(self.GENDER_TYPES).get(self.gender)
        return gender_display if gender_display else self.gender

    def get_role_display(self):
        return dict(self.Role.choices).get(self.role)


class IssueType(models.Model):
    issue = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'issue_type'

    def __str__(self):
        return self.issue


class SupportClient(models.Model):
    class Status(models.TextChoices):
        ABIERTO = "ABIERTO", "Abierto"
        EN_PROGRESO = "EN_PROGRESO", "En Progreso"
        RESUELTO = "RESUELTO", "Resuelto"
        CERRADO = "CERRADO", "Cerrado"

    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ABIERTO)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    issue_type = models.ForeignKey(IssueType, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_deleted = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'support_client'


""" class Plan(models.Model):
    plan_name = models.CharField(help_text=(
        _('Nombre del plan de suscripción')), max_length=30)
    description = models.TextField(blank=True, null=True)
    limit_requests = models.IntegerField(default=5)
    cost = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    grace_period = models.PositiveIntegerField(default=0, help_text=(
        _('Cuántos días depués de que finalice la suscripción')))
    trial_period = models.PositiveIntegerField(default=0, help_text=(
        _('Cuántos días le damos gratis antes de que la suscripción comienze')))
    sequence = models.IntegerField(
        default=0, help_text=(_('Ordenar por secuencia')))

    class Meta:
        ordering = ['sequence']
        verbose_name_plrual = "plans"

    def __str__(self):
        return self.plan_name


class Subscription(models.Model):
    STATUS_TYPE = ((0, "Activa"), (1, "Pendiente"),
                   (2, "Vencida"), (3, "Cancelada"), (4, "Suspendida"))
    status = models.SmallIntegerField(choices=STATUS_TYPE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    expiration_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    cancellation_date = models.DateTimeField()
 """
