from rest_framework.test import APITestCase

from api_routine.models import Routine
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

    def test_register_fail(self):
        username = "a@a.com"
        password = "1q2w3e4r"

        response = self.client.post("/users", data={
            "username": username,
            "password": password,
        })
        self.assertEqual(response.status_code, 400)

    def test_get_token(self):
        username = "a@a.com"
        password = "1q2w3e4r!"
        Account.objects.create_user(username=username, password=password)

        response = self.client.post("/users/token", data={
            "username": username,
            "password": password,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("refresh", response.data.keys())
        self.assertIn("access", response.data.keys())

    def test_expire_token(self):
        username = "a@a.com"
        password = "1q2w3e4r!"
        account = Account.objects.create_user(username=username, password=password)

        response = self.client.post("/users/token", data={
            "username": username,
            "password": password,
        })

        access_token = response.data["access"]
        refresh_token = response.data["refresh"]
        routine = Routine.objects.create(account=account, title="sample 1", goal="goal!")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(f"/routines/{routine.routine_id}")
        self.assertEqual(response.status_code, 200)

        self.client.post("/users/expire", data={
            "refresh": refresh_token
        })
        response = self.client.post("/users/refresh", data={
            "refresh": refresh_token
        })
        self.assertEqual(response.status_code, 401)
