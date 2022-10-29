import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from api_user.models import Account


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = ["username", "password"]

    def create(self, validated_data):
        matched_str = re.fullmatch(
            r"(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[~!@#$%^&*()_+\-=`{}\[\]<>?,./]).{8,}",
            validated_data["password"])
        if matched_str is None:
            raise ValidationError("비밀번호는 8자리 이상 영문, 숫자, 특수문자를 포함해야 합니다.")

        account = Account.objects.create_user(username=validated_data["username"], password=validated_data["password"])
        return account
