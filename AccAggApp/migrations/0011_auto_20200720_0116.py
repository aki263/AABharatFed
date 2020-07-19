# Generated by Django 3.0.8 on 2020-07-19 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccAggApp', '0010_profile_sessionid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='accountNo',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='accountRefNo',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='banklink',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='pan',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sessionid',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sid',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='txnid',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='userID',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='uuid',
        ),
        migrations.AddField(
            model_name='profile',
            name='google_auth_token',
            field=models.TextField(blank=True),
        ),
    ]
