# Generated by Django 5.0.2 on 2024-02-14 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_quotation_budget'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotation',
            old_name='property_ownership',
            new_name='ownership',
        ),
    ]