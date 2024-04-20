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

    @unittest.skip
    def test_search_by_term(self):
        print('not implemented')

    @unittest.skip
    def test_search_by_description(self):
        print('not implemented')
