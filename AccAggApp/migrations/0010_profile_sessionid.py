# Generated by Django 3.0.8 on 2020-07-19 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccAggApp', '0009_profile_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sessionid',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
