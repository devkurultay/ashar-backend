from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from assertpy import assert_that

from rest_framework_simplejwt.tokens import RefreshToken
import json

from . import factories

class TermCreationTestCase(APITestCase):
    def setUp(self):
        self.category = factories.CategoryFactory()
        self.current_user = factories.UserFactory()
        refresh = RefreshToken.for_user(self.current_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION = f'JWT {access_token}')


    def test_unauthenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'JWT wrong_access_token')

        data = {
            'term': 'чычкан',
            'description': 'Курсорду жылдырат',
            'category': self.category.slug,
            'other_lang_examples': []
        }
        response = self.client.post('/api/v1/terms/', data, format='json')

        self.assertEqual(response.status_code, 401)


    def test_insufficient_data(self):
        data = {
            'description': 'Курсорду жылдырат',
            'category': self.category.slug,
            'other_lang_examples': []
        }
        response = self.client.post('/api/v1/terms/', data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'term': ['Бул талаа керектүү.']})


    def test_create_term(self):
        data = {
            'term': 'чычкан',
            'description': 'Курсорду жылдырат',
            'category': self.category.slug,
            'other_lang_examples': []
        }

        response = self.client.post('/api/v1/terms/', data, format='json')

        expected_response = {
            'category': {'slug': 'programmaloo', 'title': 'Программалоо'},
            'description': 'Курсорду жылдырат',
            'other_language_examples': [],
            'term': 'чычкан',
            'translation_suggestions': []
        }

        self.assertEqual(response.status_code, 201)
        assert_that(json.loads(response.content)).is_equal_to(expected_response, ignore='id')
