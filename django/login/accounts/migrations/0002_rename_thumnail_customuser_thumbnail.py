# Generated by Django 5.1.4 on 2024-12-26 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='thumnail',
            new_name='thumbnail',
        ),
    ]
