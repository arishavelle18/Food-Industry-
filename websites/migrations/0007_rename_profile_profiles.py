# Generated by Django 4.1.2 on 2022-11-11 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0006_alter_profile_inspect'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='Profiles',
        ),
    ]