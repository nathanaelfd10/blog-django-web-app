# Generated by Django 5.0.6 on 2024-05-11 11:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_comment_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 11, 11, 36, 6, 178868, tzinfo=datetime.timezone.utc)),
        ),
    ]
