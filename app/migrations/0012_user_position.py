# Generated by Django 4.2.19 on 2025-04-11 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_user_licence_user_str_user_tashkiliy_huquq_shakli_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
