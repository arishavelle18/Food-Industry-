# Generated by Django 4.1.2 on 2022-11-24 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0011_alter_profiles_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personCode', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]