# Generated by Django 5.1.3 on 2024-11-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_customuser_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_subscribed',
            field=models.BooleanField(default=True),
        ),
    ]
