# Generated by Django 3.0.8 on 2020-07-17 01:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('AccAggApp', '0007_profile_banklink'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='txnid',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
