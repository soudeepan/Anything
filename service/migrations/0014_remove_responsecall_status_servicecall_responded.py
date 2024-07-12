# Generated by Django 5.0.6 on 2024-07-10 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0013_responsecall_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responsecall',
            name='status',
        ),
        migrations.AddField(
            model_name='servicecall',
            name='responded',
            field=models.BooleanField(default=False),
        ),
    ]
