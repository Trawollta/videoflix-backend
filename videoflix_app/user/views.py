from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Diese E-Mail-Adresse ist bereits vergeben.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            production_confirm_url = f"{settings.DOMAIN_FRONTEND}/confirm-email/{uid}/{token}"
            

            local_confirm_url = f"http://localhost:4200/confirm-email/{uid}/{token}"

            send_mail(
                'Bestätigen Sie Ihre E-Mail-Adresse',
                f'Bitte klicken Sie auf einen der folgenden Links, um Ihre E-Mail-Adresse zu bestätigen:\n\n'
                f'Produktionsumgebung: {production_confirm_url}\n'
                f'Lokale Entwicklungsumgebung: {local_confirm_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'Eine Bestätigungs-E-Mail wurde gesendet. Bitte überprüfen Sie Ihr Postfach.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmEmailView(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            print(uid)
            user = CustomUser.objects.get(pk=uid)
            print(f"Benutzer gefunden: {user.email}")  
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            print("Token validiert") 
            if not user.is_active:  
                user.is_active = True  
                user.save()
                print("Benutzerkonto aktiviert") 
                return Response({'message': 'E-Mail-Adresse erfolgreich bestätigt und Konto aktiviert.'}, status=status.HTTP_200_OK)
            return Response({'message': 'Benutzer ist bereits aktiviert.'}, status=status.HTTP_200_OK)
        else:
            print("Ungültiger Token oder Benutzer nicht gefunden") 
            return Response({'error': 'Ungültiger oder abgelaufener Token.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'E-Mail-Adresse ist erforderlich.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Kein Benutzer mit dieser E-Mail-Adresse gefunden.'}, status=status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.DOMAIN_FRONTEND}/reset-password-confirm/{uid}/{token}"
        send_mail(
            'Passwort zurücksetzen',
            f'Klicken Sie auf den folgenden Link, um Ihr Passwort zurückzusetzen: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({'message': 'Ein Link zum Zurücksetzen des Passworts wurde an Ihre E-Mail-Adresse gesendet.'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return Response({'uid': uidb64, 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Ungültiger oder abgelaufener Token'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.data)
            if form.is_valid():
                form.save()
                return Response({'message': 'Das Passwort wurde erfolgreich zurückgesetzt'}, status=status.HTTP_200_OK)
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Ungültiger oder abgelaufener Token'}, status=status.HTTP_400_BAD_REQUEST)
