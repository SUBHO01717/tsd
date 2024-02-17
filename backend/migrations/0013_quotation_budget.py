# Generated by Django 5.0.2 on 2024-02-14 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_quotation_images_alter_image_quotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='budget',
            field=models.CharField(choices=[('1K', '1K'), ('2K', '2K'), ('4K', '4K'), ('8K', '8K'), ('16K', '16K'), ('30K+', '30K+')], default=1, max_length=200),
            preserve_default=False,
        ),
    ]