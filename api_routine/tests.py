from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from api_routine.constants import (ROUTINE_CREATE_MESSAGE, ROUTINE_LIST_MESSAGE, ROUTINE_DETAIL_MESSAGE,
                                   ROUTINE_UPDATE_MESSAGE, ROUTINE_DELETE_MESSAGE, ROUTINE_RESULT_UPDATE_MESSAGE)
from api_routine.models import Routine, RoutineDay, RoutineResult
from api_user.models import Account


class RoutineTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = Account.objects.create_user(username="a@a.com", password="1q2w3e4r!")

    def get_temporary_routine(self):
        routine = Routine.objects.create(account=self.user,
                                         title=f"Math Problem-solving",
                                         category="HOMEWORK",
                                         goal=f"Increase your problem-solving skills",
                                         is_alarm=True)
        RoutineResult.objects.create(routine=routine)
        [RoutineDay.objects.create(routine=routine, day=day) for day in ["MON", "TUE", "FRI"]]
        return routine

    def test_register_routine(self):
        title = "Problem-solving"
        days = sorted(["MON", "WED", "FRI"])
        self.client.login(username="a@a.com", password="1q2w3e4r!")
        response = self.client.post("/routines", data={
            "title": title,
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skill",
            "is_alarm": True,
            "days": days,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"]["msg"], ROUTINE_CREATE_MESSAGE)
        self.assertTrue(Routine.objects.filter(title=title).exists())

        routine = Routine.objects.get(title=title)
        self.assertEqual(sorted(routine.days.values_list("day", flat=True)), days)

    def test_get_routines(self):
        length = 3
        for index in range(length):
            routine = self.get_temporary_routine()
            date = datetime.strptime("2022-02-22", "%Y-%m-%d") - timedelta(days=index // 2) # 짝수의 경우 과거 날짜로 생성
            routine.created_at = date
            routine.modified_at = date
            routine.save()

        self.client.login(username="a@a.com", password="1q2w3e4r!")
        response = self.client.get("/routines")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"]["msg"], ROUTINE_LIST_MESSAGE)
        self.assertEqual(len(response.data["data"]), length)

        response = self.client.get("/routines", data={
            "date": "2022-02-22"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"]["msg"], ROUTINE_DETAIL_MESSAGE)

        count = self.user.routine_set.filter(created_at__gte="2022-02-22", created_at__lt="2022-02-23").count()
        self.assertEqual(len(response.data["data"]), count)

        response = self.client.get("/routines/1")
        self.assertEqual(response.status_code, 200)

    def test_update_routines(self):
        routine = self.get_temporary_routine()

        self.client.login(username="a@a.com", password="1q2w3e4r!")
        edit_days = ["MON", "WED"]
        response = self.client.patch(f"/routines/{routine.routine_id}", data={
            "days": edit_days
        })
        self.assertEqual(response.data["message"]["msg"], ROUTINE_UPDATE_MESSAGE)
        self.assertEqual(response.status_code, 200)

        routine.refresh_from_db()
        self.assertEqual(sorted(routine.days.values_list("day", flat=True)), sorted(edit_days))

    def test_delete_routines(self):
        routine = self.get_temporary_routine()

        self.client.login(username="a@a.com", password="1q2w3e4r!")
        response = self.client.patch(f"/routines/{routine.routine_id}/delete")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"]["msg"], ROUTINE_DELETE_MESSAGE)

        routine.refresh_from_db()
        self.assertTrue(routine.is_deleted)

    def test_result_routines(self):
        routine = self.get_temporary_routine()

        edit_result = "TRY"
        self.client.login(username="a@a.com", password="1q2w3e4r!")
        response = self.client.patch(f"/routines/{routine.routine_id}/result", data={
            "result": edit_result
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"]["msg"], ROUTINE_RESULT_UPDATE_MESSAGE)

        routine.refresh_from_db()
        self.assertEqual(routine.result.result, edit_result)
