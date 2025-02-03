# Generated by Django 4.2.16 on 2025-02-03 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.CharField(max_length=36, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('secret_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='Secret Key')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
