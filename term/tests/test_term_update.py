import unittest
from rest_framework.test import APITestCase
from assertpy import assert_that

from rest_framework_simplejwt.tokens import RefreshToken
import json

from . import factories

class TermUpdateTestCase(APITestCase):
    def setUp(self):
        self.current_user = factories.UserFactory()
        refresh = RefreshToken.for_user(self.current_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION = f'JWT {access_token}')
        self.term = factories.TermFactory(author=self.current_user)


    def test_update_fields(self):
        data = {
            'term': 'new term',
            'description': 'new description',
            'active': True
        }
        path = f'/api/v1/terms/{self.term.id}/'
        response = self.client.patch(path, data, format='json')
        expected_data = {
            'id': self.term.id,
            'term': 'new term',
            'description': 'new description',
            'other_lang_examples': [],
            'category': self.term.category.slug,
            'other_language_examples': [],
            'translation_suggestions': []
        }

        assert_that(response.status_code).is_equal_to(200)
        assert_that(json.loads(response.content)).is_equal_to(expected_data, ignore='id')

    def test_update_category(self):
        category = factories.CategoryFactory(title='new category')
        data = {
            'category': category.slug
        }
        path = f'/api/v1/terms/{self.term.id}/'
        response = self.client.patch(path, data, format='json')
        expected_data = {
            'id': self.term.id,
            'term': self.term.term,
            'description': self.term.description,
            'other_lang_examples': [],
            'category': category.slug,
            'other_language_examples': [],
            'translation_suggestions': []
        }

        assert_that(response.status_code).is_equal_to(200)
        assert_that(json.loads(response.content)).is_equal_to(expected_data, ignore='id')

    def test_wrong_data(self):
        data = {
            'term': '',
            'description': 'new description',
            'active': 'True'
        }
        path = f'/api/v1/terms/{self.term.id}/'
        response = self.client.patch(path, data, format='json')


        expected_data = {
            'term': ['This field may not be blank.']
        }

        assert_that(response.status_code).is_equal_to(400)
        assert_that(json.loads(response.content)).is_equal_to(expected_data)


    def test_unauthenticated(self):
        self.client.credentials()
        data = {
            'term': 'new term',
            'description': 'new description',
            'active': True
        }
        path = f'/api/v1/terms/{self.term.id}/'
        response = self.client.patch(path, data, format='json')

        expected_data = {
            'detail': 'Authentication credentials were not provided.'
        }
        assert_that(response.status_code).is_equal_to(401)
        assert_that(json.loads(response.content)).is_equal_to(expected_data)

    def test_unauthorized(self):
        another_user = factories.UserFactory()

        another_term = factories.TermFactory(
                author=another_user,
                category=self.term.category
                )

        data = {
            'term': 'new term',
            'description': 'new description',
            'active': True
        }
        path = f'/api/v1/terms/{another_term.id}/'
        response = self.client.patch(path, data, format='json')

        expected_data = {
            'detail': 'You do not have permission to perform this action.'
        }
        assert_that(response.status_code).is_equal_to(403)
        assert_that(json.loads(response.content)).is_equal_to(expected_data)
