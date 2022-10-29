from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api_routine.models import Routine, RoutineDay, RoutineResult


class RoutineSerializer(ModelSerializer):
    result = serializers.SlugRelatedField(read_only=True, slug_field="result")
    days = serializers.SlugRelatedField(many=True, read_only=True, slug_field="day")

    class Meta:
        model = Routine
        fields = ["goal", "account_id", "title", "result", "days"]


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

    def update(self, instance, validated_data):
        with transaction.atomic():
            for key, value in validated_data.items():
                key != "days" and setattr(instance, key, value)
            instance.save()

            if validated_data.get("days"):
                instance.days.exclude(day__in=validated_data["days"]).delete()
                [RoutineDay.objects.get_or_create(routine=instance, day=day) for day in validated_data["days"]]
        return instance


class RoutineDeleteSerializer(ModelSerializer):
    class Meta:
        model = Routine
        fields = ["routine_id"]
        read_only_fields = ["routine_id"]

    def update(self, instance, validated_data):
        instance.is_deleted = True
        instance.save()
        return instance


class RoutineResultSerializer(ModelSerializer):
    result = serializers.CharField(max_length=4, write_only=True, required=True)

    class Meta:
        model = Routine
        fields = ["routine_id", "result"]

    def update(self, instance, validated_data):
        instance.result.result = validated_data["result"]
        instance.result.save()
        return instance
