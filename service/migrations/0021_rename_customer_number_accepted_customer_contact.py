# Generated by Django 5.0.6 on 2024-07-12 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0020_rename_payment_approval_service_porvider_accepted_payment_approval_service_provider'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accepted',
            old_name='customer_number',
            new_name='customer_contact',
        ),
    ]
