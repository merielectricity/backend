# Generated by Django 3.2.13 on 2022-06-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquirydata', '0003_auto_20220603_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_inquiry',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='data_inquiry',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='data_inquiry',
            name='state',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
