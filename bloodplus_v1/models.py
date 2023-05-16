from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_TYPES = (('H', 'Hombre'), ('M', 'Mujer'), ('I', 'Indefinido'))
    user = models.OneToOneField(
        User, related_name='user_profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, default='I')
    birth_date = models.DateField()
    average_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0)
    total_donations = models.PositiveIntegerField(default=0)
    total_requests = models.PositiveIntegerField(default=0)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        db_table = 'user_profile'

    def __str__(self):
        return self.user.username


