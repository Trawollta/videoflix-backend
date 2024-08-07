from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser
from django.urls import reverse
from django.conf import settings

from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwörter stimmen nicht überein.")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password1']
        )
        user.is_active = False  # Benutzer ist inaktiv, bis er bestätigt wird
        user.save()

        # Bestätigungs-E-Mail senden
        self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user):
        token = user.confirmation_token
        confirm_url = reverse('confirm-email', args=[token])
        full_url = f"{settings.DOMAIN}{confirm_url}"
        print(full_url)
        send_mail(
            'Bestätigen Sie Ihre E-Mail-Adresse',
            f'Bitte klicken Sie auf den folgenden Link, um Ihre E-Mail-Adresse zu bestätigen: {full_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Ungültige Anmeldeinformationen.")
        else:
            raise serializers.ValidationError("E-Mail und Passwort sind erforderlich.")
        data['user'] = user
        return data
