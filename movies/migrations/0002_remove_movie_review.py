# Generated by Django 3.1.4 on 2020-12-22 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='review',
        ),
    ]