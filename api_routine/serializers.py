from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_routine.models import Routine, RoutineDay, RoutineResult


class RoutineUpdateSerializer(ModelSerializer):
    days = serializers.ListField(child=serializers.CharField(max_length=3), write_only=True)

    class Meta:
        model = Routine
        fields = ["routine_id", "title", "category", "goal", "is_alarm", "days"]
        read_only_fields = ["routine_id"]

    def create(self, validated_data):
        columns = dict()
        for key, value in validated_data.items():
            key != "days" and columns.update({key: value})
        columns["account"] = self.context["request"].user

        with transaction.atomic():
            routine = Routine.objects.create(**columns)
            RoutineResult.objects.create(routine=routine)
            [RoutineDay.objects.create(routine=routine, day=day) for day in validated_data["days"]]
        return routine

