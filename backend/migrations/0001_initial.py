# Generated by Django 5.0.2 on 2024-02-09 06:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontend', '0003_subcategory_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotation_number', models.CharField(editable=False, max_length=20, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=10)),
                ('job_start', models.CharField(choices=[('Immediate', 'Immediate'), ('Within a week', 'Within a week'), ('Within two week', 'Within two week'), ('Within a month', 'Within a month'), ('Within two month', 'Within two month'), ('Flexible Date', 'Flexible Date')], default='Immediate', max_length=50)),
                ('stage', models.CharField(choices=[('I am ready to hire ', 'I am ready to hire '), ("I'm palning & budgeting ", "I'm palning & budgeting "), ('I need a qoute for Insurance ', 'I need a qoute for Insurance ')], default='I am ready to hire', max_length=200)),
                ('property_ownership', models.CharField(choices=[('I own and live at this property ', 'I own and live at this property'), ("I'm a Landlord ", "I'm a Landlord"), ("I'm a tenent but authorize to change", "I'm a tenent but authorize to change"), ("I'm planing to buy", "I'm planing to buy")], default="I'm a Landlord ", max_length=200)),
                ('job_details', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Replied', 'Replied'), ('Win', 'Win'), ('Lost', 'Lost'), ('Not Interested', 'Not Interested')], default='Pending', max_length=50)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.category')),
                ('subCategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frontend.subcategory')),
            ],
        ),
    ]