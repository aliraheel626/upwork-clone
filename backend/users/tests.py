from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class UserAuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.token_url = reverse('token')
        self.me_url = reverse('user')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'], self.user_data['username'])

    def test_user_login(self):
        """Test user login and token generation"""
        # Register the user first
        self.client.post(self.register_url, self.user_data, format='json')

        # Login to obtain token
        response = self.client.post(
            self.token_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_me_endpoint(self):
        """Test /me endpoint with and without token"""
        # Register and login to get access token
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(
            self.token_url, self.user_data, format='json')
        access_token = login_response.data['access']

        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Access /me endpoint
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['id'], User.objects.get(
            username=self.user_data['username']).id)

        # Test accessing /me endpoint without token
        self.client.credentials()  # Remove token
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_refresh_token(self):
        """Test token refresh endpoint"""
        # Register and login to get refresh token
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(
            self.token_url, self.user_data, format='json')
        refresh_token = login_response.data['refresh']

        # Refresh token
        refresh_url = reverse('token-refresh')
        response = self.client.post(
            refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
