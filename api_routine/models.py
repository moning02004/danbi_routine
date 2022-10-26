from django.contrib.auth import get_user_model
from django.db import models


class Routine(models.Model):
    routine_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    category = models.CharField(max_length=8, choices=(
        ("MIRACLE", "기상 관련"), ("HOMEWORK", "숙제 관련")
    ))
    goal = models.CharField(max_length=200, null=False)
    is_alarm = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "routine"


class RoutineResult(models.Model):
    routine_result_id = models.BigAutoField(primary_key=True)
    routine = models.OneToOneField(Routine, on_delete=models.CASCADE, related_name="result")

    result = models.CharField(max_length=4, default="NOT", choices=(
        ("NOT", "안함"), ("TRY", "시도"), ("DONE", "완료")
    ))
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "routine_result"


class RoutineDay(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="days")
    day = models.CharField(max_length=3)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "routine_day"
        unique_together = ("day", "routine")
