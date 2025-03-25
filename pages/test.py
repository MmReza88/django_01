from django.test import TestCase, SimpleTestCase


class SimpleTest (SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)


    def test_home_page_status_code(self):
        response = self.client.get('/sub_01/')
        self.assertEqual(response.status_code,200)

