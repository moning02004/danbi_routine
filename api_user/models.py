from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    username = models.EmailField(unique=True)

    class Meta:
        db_table = "account"
