# Generated by Django 4.1.3 on 2023-04-02 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0003_profile_email_alter_profile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]