# Generated by Django 3.0.8 on 2020-07-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('AccAggApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pan',
            field=models.CharField(default=0, max_length=11),
            preserve_default=False,
        ),
    ]
