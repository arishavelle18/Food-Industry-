# Generated by Django 4.1.2 on 2023-01-11 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminportal', '0005_user_auth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth',
            field=models.BooleanField(null=True),
        ),
    ]
