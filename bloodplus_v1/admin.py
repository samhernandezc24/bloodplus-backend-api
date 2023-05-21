from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    """Un formulario para actualizar usuarios. Incluye todos los campos de
    usuario, pero reemplaza el campo de contraseña por el campo de visualización de hash de contraseña deshabilitada de admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "password", "date_of_birth", "is_active"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        'email', 'username', 'first_name', 'last_name', 'date_of_birth', 'is_active', 'date_joined']
    list_filter = ['email', 'is_active']
    fieldsets = [
        (None, {"fields": ["email", "username", "first_name", "last_name", "password"]}),
        ("Información Personal", {"fields": ["date_of_birth", "gender", "phone"]}),
    ]
    # add_fieldsets no es un atributo estándar de ModelAdmin. UserAdmin
    # anula get_fieldsets para usar este atributo cuando se crea un usuario.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "first_name", "last_name", "email", "username", 
                    "password1", "password2", "date_of_birth", "is_active",
                    "is_superuser"
                ],
            },
        ),
    ]
    ordering = ['-date_joined']
    filter_horizontal = []

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)