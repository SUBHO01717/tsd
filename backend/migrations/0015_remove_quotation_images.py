# Generated by Django 5.0.2 on 2024-02-15 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_rename_property_ownership_quotation_ownership'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='images',
        ),
    ]
