# Generated by Django 5.0.2 on 2024-02-16 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_jobapplication_alter_job_details'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JobApplication',
        ),
    ]