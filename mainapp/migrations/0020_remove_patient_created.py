# Generated by Django 3.1.1 on 2020-10-01 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_patient_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='created',
        ),
    ]
