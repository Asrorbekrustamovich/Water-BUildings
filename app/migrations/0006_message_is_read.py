# Generated by Django 4.2.19 on 2025-02-24 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_user_adress'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
