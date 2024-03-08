from rest_framework.test import APITestCase
from assertpy import assert_that

import json

from . import factories

class TermListingTestCase(APITestCase):
    def test_list_terms(self):
        term = factories.TermFactory()
        response = self.client.get('/api/v1/terms/')

        expected_response = [
            {
                'category': {'slug': 'programmaloo', 'title': 'Программалоо'},
                'description': term.description,
                'id': term.id,
                'other_language_examples': [],
                'term': 'процессор',
                'translation_suggestions': []
            }
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)
