# Generated by Django 5.1.3 on 2025-02-07 11:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("friend_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="friends",
            name="approved_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="friends",
            name="request_sent_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
