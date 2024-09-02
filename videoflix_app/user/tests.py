from django.urls import reverse
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class RegistrationsTestCase(APITestCase):

    def setUp(self):
        
        self.user = get_user_model().objects.create_user(
            email= 'testuser@example.com',
            password='testpassword'
        )

    def test_user_registration(self):
        data = {
            "email": 'testuser1@example.com',
            "password1":'testpassword',
            "password2":'testpassword'
        }
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.filter(email=data['email']).count(), 1)
        self.assertIn('Eine Bestätigungs-E-Mail wurde gesendet', response.data['message'])

    def test_user_registration_password_mismatch(self):
        data = {
            "email": 'testuser2@example.com',
            "password1": 'testpassword',
            "password2": 'differentpassword'
        }
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Passwörter stimmen nicht überein', response.data['non_field_errors'][0])
        

class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            is_active=True 
        )

    def test_login(self):
        
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {'email': self.user.email, 'password': 'wrongpassword'}, format='json')
        self.assertIn('non_field_errors', response.data)
        self.assertIn('Ungültige Anmeldeinformationen', response.data['non_field_errors'][0])

class EmailConfirmationTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword'
        )
        self.user.is_active = False
        self.user.save()

    def test_confirm_email(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(reverse('confirm-email', args=[uid, token]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_confirm_email_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = 'invalid-token'
        response = self.client.get(reverse('confirm-email', args=[uid, token]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Ungültiger oder abgelaufener Token.', response.data['error'])


class PasswordResetTestCase(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            is_active=True 
        )

    def test_password_reset(self):
        response = self.client.post(reverse('password-reset'), {'email': self.user.email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Ein Link zum Zurücksetzen des Passworts wurde an Ihre E-Mail-Adresse gesendet', response.data['message'])

    def test_password_reset_confirm(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(reverse('password_reset_confirm', args=[uid, token]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
       
        response = self.client.post(reverse('password_reset_confirm', args=[uid, token]), {
            'new_password1': 'newpassword',
            'new_password2': 'newpassword'
        }, format='json')
        print(response.data) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))

    def test_password_reset_confirm(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(reverse('password_reset_confirm', args=[uid, token]), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        response = self.client.post(reverse('password_reset_confirm', args=[uid, token]), {
            'new_password1': 'sicheresPasswort123',
            'new_password2': 'sicheresPasswort123'
        }, format='json')
        
        print(f"Antwortdaten: {response.data}") 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('sicheresPasswort123'))



