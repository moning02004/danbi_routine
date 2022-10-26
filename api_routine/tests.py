from rest_framework.test import APITestCase

from api_routine.models import Routine, RoutineDay, RoutineResult
from api_user.models import Account


class RoutineTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = Account.objects.create_user(username="a@a.com", password="1q2w3e4r!")

    def test_register_routine(self):
        title = "Problem-solving"

        self.client.login(username="a@a.com", password="1q2w3e4r!")
        response = self.client.post("/routines", data={
            "title": title,
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skill",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"],
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Routine.objects.filter(title=title).exists())

        routine = Routine.objects.get(title=title)
        self.assertEqual(RoutineDay.objects.filter(routine=routine).count(), 3)

    def test_get_routines(self):
        for index in range(2):
            routine = Routine.objects.create(account=self.user,
                                             title=f"Math Problem-solving {index}",
                                             category="HOMEWORK",
                                             goal=f"Increase your problem-sovling skills {index}",
                                             is_alarm=True)
            RoutineResult.objects.create(routine=routine)
            [RoutineDay.objects.create(routine=routine, day=day) for day in ["MON", "TUE", "FRI"]]

        self.client.login(username="a@a.com", password="1q2w3e4r!")
        response = self.client.get("/routines")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
