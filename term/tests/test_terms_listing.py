import unittest
from rest_framework.test import APITestCase
from assertpy import assert_that

import json

from . import factories

class TermListingTestCase(APITestCase):
    def setUp(self):
        self.term = factories.TermFactory()

    def test_list_terms(self):
        response = self.client.get('/api/v1/terms/')

        expected_response = [
            {
                'category': {'slug': 'programmaloo', 'title': 'Программалоо'},
                'description': self.term.description,
                'id': self.term.id,
                'other_language_examples': [],
                'term': 'процессор',
                'translation_suggestions': []
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)


    def test_filter_by_category(self):
        category = factories.CategoryFactory(title='администрлөө')
        factories.TermFactory(category=category)

        response = self.client.get('/api/v1/terms/?filter=programmaloo')

        expected_response = [
            {
                'category': {'slug': 'programmaloo', 'title': 'Программалоо'},
                'description': self.term.description,
                'id': self.term.id,
                'other_language_examples': [],
                'term': 'процессор',
                'translation_suggestions': []
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)

    def test_search_by_term(self):
        second_term = factories.TermFactory(term='процессорлор', category=self.term.category)
        response = self.client.get('/api/v1/terms/?search=процессор')

        expected_response = [
            {
                'category': {'slug': 'programmaloo', 'title': 'Программалоо'},
                'description': self.term.description,
                'id': self.term.id,
                'other_language_examples': [],
                'term': 'процессор',
                'translation_suggestions': []
            },
            {
                'category': {'slug': 'programmaloo', 'title': 'Программалоо'},
                'description': second_term.description,
                'id': second_term.id,
                'other_language_examples': [],
                'term': 'процессорлор',
                'translation_suggestions': []
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)

    def test_search_by_description(self):
        second_term = factories.TermFactory(
                term='cpu',
                description='компьютердеги процессор',
                category=self.term.category
        )
        response = self.client.get('/api/v1/terms/?search=компьютер')

        expected_response = [
            {
                'category': {'slug': 'programmaloo', 'title': 'Программалоо'},
                'description': second_term.description,
                'id': second_term.id,
                'other_language_examples': [],
                'term': 'cpu',
                'translation_suggestions': []
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
