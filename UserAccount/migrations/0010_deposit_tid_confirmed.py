# Generated by Django 3.2 on 2022-08-22 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0009_auto_20220821_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='deposit',
            name='tid_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
