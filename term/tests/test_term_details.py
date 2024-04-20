import unittest
from rest_framework.test import APITestCase
from assertpy import assert_that

import json

from . import factories

class TermDetailsTestCase(APITestCase):

    def test_term_details(self):
        user = factories.UserFactory()
        category = factories.CategoryFactory()
        term = factories.TermFactory(author=user, category=category)

        response = self.client.get(f'/api/v1/term/{term.id}/')
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.data).is_equal_to({
            'id': term.id,
            'term': term.term,
            'description': term.description,
            'category': {
                'slug': category.slug,
                'title': category.title,
            }
        }, ignore=['other_language_examples','translation_suggestions'])
