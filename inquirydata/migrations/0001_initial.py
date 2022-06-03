# Generated by Django 3.2.13 on 2022-06-03 11:48

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='data_inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', phone_field.models.PhoneField(help_text='Contact phone number', max_length=31)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=40)),
                ('pincode', models.IntegerField()),
                ('existing_plant', models.BooleanField()),
                ('plant_size', models.IntegerField(blank=True, null=True)),
                ('geo_location', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
