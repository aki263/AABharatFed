# Generated by Django 3.0.8 on 2020-07-16 23:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('AccAggApp', '0005_profile_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sid',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
