# Generated by Django 5.1.3 on 2024-11-07 10:53

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0003_alter_category_options_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(),
        ),
    ]
