from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from api_routine.models import Routine, RoutineDay, RoutineResult
from api_user.models import Account


class RoutineTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(username="a@a.com", password="1q2w3e4r!")

    def get_temporary_routine(self):
        routine = Routine.objects.create(account=self.user,
                                         title=f"Math Problem-solving",
                                         category="HOMEWORK",
                                         goal=f"Increase your problem-sovling skills",
                                         is_alarm=True)
        RoutineResult.objects.create(routine=routine)
        [RoutineDay.objects.create(routine=routine, day=day) for day in ["MON", "TUE", "FRI"]]
        return routine

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
        length = 3
        for index in range(length):
            routine = self.get_temporary_routine()
            date = datetime.strptime("2022-02-22", "%Y-%m-%d") - timedelta(days=index)
            routine.created_at = date
            routine.modified_at = date
            routine.save()

        self.client.login(username="a@a.com", password="1q2w3e4r!")
        response = self.client.get("/routines")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), length)

        response = self.client.get("/routines", data={
            "date": "2022-02-22"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)

        single_response = self.client.get("/routines/1")
        self.assertEqual(single_response.status_code, 200)

    def test_update_routines(self):
        routine = self.get_temporary_routine()

        self.client.login(username="a@a.com", password="1q2w3e4r!")
        edit_days = ["MON", "WED"]
        response = self.client.patch(f"/routines/{routine.routine_id}", data={
            "days": edit_days
        })
        self.assertEqual(response.status_code, 200)

        routine.refresh_from_db()
        self.assertEqual(sorted(routine.days.values_list("day", flat=True)), sorted(edit_days))

    def test_delete_routines(self):
        routine = self.get_temporary_routine()

        self.client.login(username="a@a.com", password="1q2w3e4r!")
        response = self.client.delete(f"/routines/{routine.routine_id}")
        self.assertEqual(response.status_code, 204)

        self.assertFalse(Routine.objects.filter(routine_id=routine.routine_id).exists())
