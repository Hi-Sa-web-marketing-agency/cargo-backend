# Generated by Django 5.0.6 on 2024-05-09 07:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0002_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='salesman',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
