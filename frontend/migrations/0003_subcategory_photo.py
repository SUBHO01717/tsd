# Generated by Django 5.0.2 on 2024-02-08 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_remove_category_specialization'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='photo',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='media/category'),
        ),
    ]