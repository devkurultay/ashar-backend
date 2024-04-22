from rest_framework.test import APITestCase
from assertpy import assert_that

import json

from . import factories

class CategoryListingTestCase(APITestCase):
    def test_list_terms(self):
        factories.CategoryFactory()
        response = self.client.get('/api/v1/categories/')

        expected_response = [
            {
                'slug': 'programmaloo',
                'title': 'Программалоо'
            },
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), expected_response)

