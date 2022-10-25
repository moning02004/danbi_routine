from rest_framework.test import APITestCase

from api_user.models import Account


class UserTestCase(APITestCase):

    def test_register_user(self):
        username = "a@a.com"
        password = "1q2w3e4r!"

        response = self.client.post("/users", data={
            "username": username,
            "password": password,
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Account.objects.filter(username=username).exists())