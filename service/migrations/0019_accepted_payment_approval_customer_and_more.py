# Generated by Django 5.0.6 on 2024-07-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0018_accepted_service_approval_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted',
            name='payment_approval_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='accepted',
            name='payment_approval_service_porvider',
            field=models.BooleanField(default=False),
        ),
    ]
