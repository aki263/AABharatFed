# Generated by Django 3.0.8 on 2020-07-19 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccAggApp', '0012_auto_20200720_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_auth_token', models.TextField(blank=True)),
            ],
        ),
    ]