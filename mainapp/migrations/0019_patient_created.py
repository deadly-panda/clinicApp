# Generated by Django 3.1.1 on 2020-10-01 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_document_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
