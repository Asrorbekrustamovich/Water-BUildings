# Generated by Django 4.2.19 on 2025-03-07 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_user_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
    ]
