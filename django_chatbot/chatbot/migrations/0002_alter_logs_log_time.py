# Generated by Django 4.2.3 on 2023-12-19 19:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='log_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
