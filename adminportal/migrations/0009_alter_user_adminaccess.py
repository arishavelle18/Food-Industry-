# Generated by Django 4.1.2 on 2023-01-16 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminportal', '0008_alter_user_adminaccess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='adminAccess',
            field=models.BooleanField(null=True),
        ),
    ]
