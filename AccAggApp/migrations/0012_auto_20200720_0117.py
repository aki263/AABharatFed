# Generated by Django 3.0.8 on 2020-07-19 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AccAggApp', '0011_auto_20200720_0116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='google_auth_token',
        ),
        migrations.AddField(
            model_name='profile',
            name='accountNo',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='accountRefNo',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='banklink',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='mobile',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='pan',
            field=models.CharField(default=1, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='sessionid',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='profile',
            name='sid',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='txnid',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='userID',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='uuid',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
