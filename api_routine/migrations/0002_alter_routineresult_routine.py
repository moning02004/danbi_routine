# Generated by Django 4.1.2 on 2022-10-25 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_routine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routineresult',
            name='routine',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api_routine.routine'),
        ),
    ]
